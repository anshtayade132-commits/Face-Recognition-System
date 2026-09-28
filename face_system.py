import cv2
import face_recognition
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor(dictionary=True)

print("Database connected successfully!")

script_folder = os.path.dirname(os.path.abspath(__file__))
faces_folder = os.path.join(script_folder, "faces")
os.makedirs(faces_folder, exist_ok=True)

print("\nFACE REGISTRATION")
register = input("Do you want to register a new face? (y/n): ").lower()

if register == "y":

    person_id = input("Enter Person ID (example P001): ").strip().upper()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open webcam.")
        cursor.close()
        connection.close()
        exit()

    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    print("\nLook at the camera.")
    print("Press S to save the face.")
    print("Press Q to cancel.")

    while True:

        ret, frame = camera.read()

        if not ret:
            print("Camera error.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s") and len(faces) > 0:

            x, y, w, h = faces[0]

            face = frame[y:y+h, x:x+w]

            filename = os.path.join(
                faces_folder,
                f"{person_id}.jpg"
            )

            cv2.imwrite(filename, face)

            print(f"\nFace saved successfully: {filename}")

            break

        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

print("\nLOADING REGISTERED FACES")

known_encodings = []
known_ids = []

for filename in os.listdir(faces_folder):

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        person_id = os.path.splitext(filename)[0]

        image_path = os.path.join(
            faces_folder,
            filename
        )

        print("Loading:", image_path)

        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:

            known_encodings.append(encodings[0])
            known_ids.append(person_id)

            print("Face loaded:", person_id)

        else:

            print("No face found:", filename)

print("\nKnown faces:", known_ids)

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("Could not open webcam.")

    cursor.close()
    connection.close()

    exit()

print("\nFACE RECOGNITION STARTED")
print("Press Q to quit.")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Failed to read camera.")
        break

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    face_locations = face_recognition.face_locations(
        rgb_frame
    )

    face_encodings = face_recognition.face_encodings(
        rgb_frame,
        face_locations
    )

    for (top, right, bottom, left), face_encoding in zip(
        face_locations,
        face_encodings
    ):

        person_id = None
        details = None

        if len(known_encodings) > 0:

            face_distances = face_recognition.face_distance(
                known_encodings,
                face_encoding
            )

            best_match_index = face_distances.argmin()

            best_distance = face_distances[best_match_index]

            print(
                "Face distance:",
                round(float(best_distance), 3)
            )

            if best_distance < 0.6:

                person_id = known_ids[best_match_index]

                cursor.execute(
                    """
                    SELECT *
                    FROM persons
                    WHERE person_id = %s
                    """,
                    (person_id,)
                )

                details = cursor.fetchone()

        if details:

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

            information = [
                f"ID: {details['person_id']}",
                f"Name: {details['name']}",
                f"Age: {details['age']}",
                f"Gender: {details['gender']}",
                f"Phone: {details['phone']}",
                f"Email: {details['email']}",
                f"City: {details['city']}"
            ]

            y = top - 10

            for info in information:

                y -= 25

                if y < 20:
                    y = bottom + 25

                cv2.putText(
                    frame,
                    info,
                    (left, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        else:

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                "Unknown Person",
                (left, bottom + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

    cv2.imshow(
        "Face Recognition System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cursor.close()
connection.close()
cv2.destroyAllWindows()

print("\nProgram closed.")