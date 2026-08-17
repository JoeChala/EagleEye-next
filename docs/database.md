# Database

## Student
- purpose: Store the identity and academic information of a student.
- fields: id, roll_number, name, email, department, semester, section, is_active, created_at, updated_at, deleted_at
- unique fields: roll_number
- constraints: roll_number must be unique; is_active defaults to true; deleted_at is nullable for soft deletion.
- relationships: 1 to N with FaceProfile; 1 to N with AttendanceRecord

## FaceProfile
- purpose: Represent a student's enrolled facial identity separately from the actual vector embeddings.
- fields: id, student_id, status, created_at, updated_at
- unique fields: id
- constraints: student_id must reference an existing student; optionally enforce one active profile per student.
- relationships: N to 1 with Student; 1 to N with FaceEmbedding; 1 to N with FaceImage

## FaceEmbedding
- purpose: Store metadata and references for a facial embedding used by the vector-search system.
- fields: id, face_profile_id, provider, collection, vector_id, model_name, model_version, dimension, pose, quality_score, created_at
- unique fields: id, vector_id
- constraints: vector_id must uniquely identify the vector within its provider/collection; embeddings must use a known model and dimension; face_profile_id must reference an existing profile.
- relationships: N to 1 with FaceProfile

## FaceImage
- purpose: Store metadata about the images used to enroll or validate a student's face; the actual image is stored in object storage.
- fields: id, face_profile_id, storage_key, pose, quality_score, created_at
- unique fields: id
- constraints: storage_key must identify the stored image; face_profile_id must reference an existing profile.
- relationships: N to 1 with FaceProfile

## AttendanceSession
- purpose: Represent a specific class/session during which attendance is recorded.
- fields: id, subject, teacher_id, department, semester, section, start_time, end_time, status, created_at, updated_at
- unique fields: id
- constraints: start_time must occur before end_time; teacher_id must reference a valid user; a session belongs to a specific academic context.
- relationships: N to 1 with User; 1 to N with AttendanceRecord

## AttendanceRecord
- purpose: Store the attendance result of one student for one attendance session.
- fields: id, session_id, student_id, status, marked_at, source, confidence, created_at, updated_at
- unique fields: id
- constraints: (session_id, student_id) must be unique; session_id and student_id must reference existing records; confidence should be nullable because manually recorded attendance may not have a recognition confidence.
- relationships: N to 1 with AttendanceSession; N to 1 with Student

## User
- purpose: Represent people who operate and manage the EagleEye system.
- fields: id, name, email, password_hash, role, is_active, created_at, updated_at, deleted_at
- unique fields: email
- constraints: email must be unique; password must never be stored directly; inactive users cannot authenticate.
- relationships: 1 to N with AttendanceSession as teacher/creator; 1 to N with AuditLog later

## Vector Store
- purpose: Store and search high-dimensional face embeddings without coupling the application to a specific vector database.
- fields: provider, collection, vector_id, embedding, metadata
- unique fields: vector_id within a provider/collection
- constraints: face vectors and document vectors should use separate collections; vector dimension must match the embedding model; the relational database stores the reference to the vector rather than depending on the vector implementation.
- relationships: logically associated with FaceEmbedding; the vector store itself is not a relational entity