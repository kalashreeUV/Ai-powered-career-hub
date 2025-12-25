from fpdf import FPDF

def create_pdf(topic, questions_answers, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 10, f"{topic} Interview Questions & Answers", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Times", "", 12)
    for i, (q, a) in enumerate(questions_answers, 1):
        pdf.set_font("Times", "B", 12)
        pdf.multi_cell(0, 8, f"{i}. {q}")
        pdf.set_font("Times", "", 12)
        pdf.multi_cell(0, 8, f"Answer: {a}")
        pdf.ln(3)
    
    pdf.output(filename)
    print(f"{filename} created successfully!")

# ====================== QUESTIONS & ANSWERS ======================
python_qna = [
    ("What is Python?", "Python is a high-level, interpreted language."),
    ("Difference between list and tuple?", "List is mutable, tuple is immutable."),
    ("What is a Python decorator?", "Function that modifies another function."),
    ("Explain Python's GIL.", "Global Interpreter Lock allows one thread at a time."),
    ("What are Python generators?", "Functions that yield a sequence of values."),
    ("What is list comprehension?", "Concise way to create lists."),
    ("What are Python modules?", "Files containing Python code to import."),
    ("Explain lambda functions.", "Anonymous single-expression functions."),
    ("Shallow copy vs deep copy?", "Shallow copies references; deep copies objects."),
    ("What is __init__?", "Constructor method for initializing objects."),
    ("Explain try/except.", "For exception handling."),
    ("What is the 'with' statement?", "Context manager for resources."),
    ("List vs set vs dict?", "List: ordered, duplicates; Set: unique; Dict: key-value."),
    ("What is 'pass'?", "Null operation placeholder."),
    ("What is docstring?", "String literal documenting code."),
    ("What are iterators?", "Objects to traverse elements."),
    ("Python 2 vs 3?", "Python 3 uses Unicode by default."),
    ("What is Python's object reference?", "Variables hold object references."),
    ("What is Python's import system?", "Loads modules into the current namespace."),
    ("Explain Python's memory management.", "Automatic garbage collection.")
]

java_qna = [
    ("What is Java?", "Java is a high-level, object-oriented, platform-independent language."),
    ("Difference between JDK, JRE, JVM?", "JDK: development kit; JRE: runtime environment; JVM: virtual machine."),
    ("What is a Class and Object?", "Class is a blueprint; object is an instance of a class."),
    ("Explain method overloading.", "Multiple methods with same name but different parameters."),
    ("Explain method overriding.", "Subclass provides specific implementation of a parent method."),
    ("What is JVM heap?", "Memory area for object storage."),
    ("What is garbage collection?", "Automatic memory management process."),
    ("What are Java interfaces?", "Abstract types with method signatures."),
    ("Difference between abstract class and interface?", "Abstract class can have implementation; interface cannot (Java 7)."),
    ("What is the 'final' keyword?", "Indicates constant value or non-overridable method."),
    ("What is Java exception handling?", "Try, catch, finally blocks to handle errors."),
    ("Difference between checked and unchecked exceptions?", "Checked: compile-time; unchecked: runtime."),
    ("What is multithreading?", "Concurrent execution of threads."),
    ("What is synchronization?", "Controlling access to shared resources in multithreading."),
    ("Explain Java Collections Framework.", "Provides data structures like List, Set, Map."),
    ("Difference between ArrayList and LinkedList?", "ArrayList: index-based; LinkedList: node-based."),
    ("What is Java Stream API?", "Process collections in functional style."),
    ("Explain JIT compiler.", "Just-In-Time compiler improves performance at runtime."),
    ("What is serialization?", "Converting object to byte stream."),
    ("What is Java reflection?", "Ability to inspect and modify classes at runtime.")
]

sql_qna = [
    ("What is SQL?", "Structured Query Language used to manage relational databases."),
    ("Difference between SQL and MySQL?", "SQL: language; MySQL: relational database software."),
    ("What is a primary key?", "Unique identifier for a table record."),
    ("What is a foreign key?", "Column linking to primary key in another table."),
    ("Explain JOIN types.", "INNER, LEFT, RIGHT, FULL joins combine tables."),
    ("What is normalization?", "Organizing tables to reduce redundancy."),
    ("Difference between clustered and non-clustered index?", "Clustered: sorts table data; Non-clustered: separate index."),
    ("What is a view?", "Virtual table created by query."),
    ("What is a stored procedure?", "Precompiled SQL code block."),
    ("What is a trigger?", "SQL code executed automatically on events."),
    ("Explain ACID properties.", "Atomicity, Consistency, Isolation, Durability."),
    ("What is a transaction?", "Unit of work that must be committed or rolled back."),
    ("What is a subquery?", "Query within a query."),
    ("What is GROUP BY?", "Aggregates rows sharing a column value."),
    ("What is HAVING clause?", "Filters groups after aggregation."),
    ("Difference between DELETE and TRUNCATE?", "DELETE: row-by-row; TRUNCATE: fast table clear."),
    ("What is indexing?", "Technique to speed up queries."),
    ("What is a union vs union all?", "Union removes duplicates; union all keeps all."),
    ("What is a schema?", "Database structure definition."),
    ("Explain foreign key constraints.", "Maintains referential integrity between tables.")
]

c_qna = [
    ("What is C?", "C is a procedural programming language developed by Dennis Ritchie."),
    ("Difference between C and C++?", "C is procedural; C++ supports OOP."),
    ("What is a pointer?", "Variable storing memory address."),
    ("What is a null pointer?", "Pointer pointing to no valid memory."),
    ("Difference between malloc() and calloc()?", "Malloc: uninitialized; Calloc: zero-initialized."),
    ("What is segmentation fault?", "Accessing invalid memory."),
    ("What are storage classes?", "auto, register, static, extern."),
    ("What is the difference between structure and union?", "Structure: all members occupy memory separately; Union: shares memory."),
    ("Explain recursion.", "Function calling itself."),
    ("What is a static variable?", "Variable that retains value across function calls."),
    ("What is a header file?", "Contains function declarations and macros."),
    ("What is the difference between = and ==?", "= assigns; == compares."),
    ("What is a constant?", "Fixed value that cannot be changed."),
    ("Explain arrays.", "Collection of elements of same type."),
    ("What is a function pointer?", "Pointer storing address of a function."),
    ("Difference between call by value and call by reference?", "Value: copy passed; Reference: original variable passed."),
    ("What is typedef?", "Defines new name for existing type."),
    ("What is preprocessor?", "Runs before compilation (#include, #define)."),
    ("Difference between break and continue?", "Break: exit loop; Continue: skip iteration."),
    ("What is a macro?", "Preprocessor directive replaced before compilation.")
]

cpp_qna = [
    ("What is C++?", "C++ is an extension of C supporting object-oriented programming."),
    ("What is a class?", "Blueprint for creating objects."),
    ("What is an object?", "Instance of a class."),
    ("Explain constructors and destructors.", "Constructor: initializes; Destructor: cleans up."),
    ("What is inheritance?", "Mechanism to derive new class from existing class."),
    ("What is polymorphism?", "Ability of object to take many forms."),
    ("What is encapsulation?", "Hiding data using access specifiers."),
    ("What is abstraction?", "Hiding implementation details from user."),
    ("What is virtual function?", "Function allowing runtime polymorphism."),
    ("Difference between overloading and overriding?", "Overloading: compile-time; Overriding: runtime."),
    ("What is operator overloading?", "Redefining operator behavior for classes."),
    ("What is a template?", "Generic programming for functions/classes."),
    ("What is namespace?", "Container to avoid name conflicts."),
    ("Difference between stack and heap?", "Stack: function calls; Heap: dynamic memory."),
    ("What is a pointer?", "Variable storing memory address."),
    ("Explain reference variables.", "Alias for another variable."),
    ("What is dynamic memory allocation?", "Allocating memory at runtime."),
    ("Difference between shallow and deep copy?", "Shallow: references shared; Deep: copies data."),
    ("What is friend function?", "Can access private members of a class."),
    ("What is RTTI?", "Run-time type information.")
]

django_qna = [
    ("What is Django?", "High-level Python web framework for rapid development."),
    ("What are Django models?", "Python classes representing database tables."),
    ("What are Django views?", "Functions/classes handling HTTP requests."),
    ("What is Django template?", "HTML with placeholders for dynamic content."),
    ("Explain Django ORM.", "Object-relational mapping to interact with DB using Python."),
    ("What is a Django app?", "Component/module of a Django project."),
    ("What is a Django project?", "Collection of apps with settings and configuration."),
    ("Explain URL routing in Django.", "Mapping URLs to views using urls.py."),
    ("What are Django forms?", "Handle input validation and rendering forms."),
    ("What is Django admin?", "Automatic interface to manage site data."),
    ("What is a Django middleware?", "Hooks to process request/response globally."),
    ("What is Django session?", "Server-side storage for user data."),
    ("What is Django static files?", "CSS, JS, images served with project."),
    ("Difference between GET and POST in Django?", "GET: fetch; POST: submit data."),
    ("What is Django signals?", "Allow decoupled apps to get notified on events."),
    ("Explain Django authentication.", "Built-in user login and permission system."),
    ("What is CSRF?", "Cross-site request forgery protection in forms."),
    ("What is Django caching?", "Storing results for faster retrieval."),
    ("What are Django management commands?", "Custom commands for project maintenance."),
    ("Difference between Django and Flask?", "Django: full-featured; Flask: lightweight microframework.")
]

mongodb_qna = [
    ("What is MongoDB?", "NoSQL document-oriented database."),
    ("Difference between SQL and NoSQL?", "SQL: relational; NoSQL: non-relational."),
    ("What is a document in MongoDB?", "Data stored in BSON format, similar to JSON."),
    ("What is a collection?", "Group of MongoDB documents."),
    ("Explain _id field.", "Unique identifier for each document."),
    ("What is replication in MongoDB?", "Multiple copies of data for high availability."),
    ("What is sharding?", "Horizontal partitioning of data across servers."),
    ("What are indexes?", "Optimize queries for faster retrieval."),
    ("Explain aggregation framework.", "Pipeline operations to process data."),
    ("What is MongoDB schema?", "Optional structure for documents."),
    ("Difference between embedded and referenced documents?", "Embedded: nested; Referenced: linked by id."),
    ("What is capped collection?", "Fixed-size collection with insertion order preserved."),
    ("Explain GridFS.", "Store large files in chunks."),
    ("Difference between find() and findOne().", "find(): multiple docs; findOne(): single doc."),
    ("What is TTL index?", "Automatically deletes documents after a time."),
    ("Explain update operators.", "$set, $inc, $push, etc."),
    ("What is Mongo shell?", "Interactive JavaScript interface for DB."),
    ("What is change stream?", "Watch for real-time changes in data."),
    ("What is MongoDB Atlas?", "Cloud-hosted MongoDB service."),
    ("What is a replica set?", "Group of mongod instances for redundancy and failover.")
]

banking_qna = [
    ("What is banking?", "Banking is the business of accepting deposits and lending money."),
    ("What are the types of banks?", "Commercial, retail, investment, central, cooperative."),
    ("What is a savings account?", "Account to deposit money and earn interest."),
    ("What is a current account?", "Account for business transactions with no interest."),
    ("What is NEFT?", "National Electronic Funds Transfer system."),
    ("What is RTGS?", "Real-Time Gross Settlement system."),
    ("What is SWIFT?", "International financial messaging system."),
    ("What is KYC?", "Know Your Customer process for identity verification."),
    ("What is a credit score?", "Numeric rating representing creditworthiness."),
    ("What is a loan?", "Borrowed money to be repaid with interest."),
    ("Difference between secured and unsecured loans?", "Secured: backed by collateral; Unsecured: no collateral."),
    ("What is interest rate?", "Percentage charged on borrowed money."),
    ("What is a bank draft?", "Instrument to transfer money safely."),
    ("What is a cheque?", "Written order to pay money."),
    ("What is digital banking?", "Banking through online/mobile platforms."),
    ("What is inflation?", "General increase in prices over time."),
    ("What is repo rate?", "Rate at which central bank lends to commercial banks."),
    ("What is reverse repo rate?", "Rate at which central bank borrows from commercial banks."),
    ("What is capital adequacy ratio?", "Minimum capital a bank must maintain."),
    ("What is liquidity ratio?", "Measure of bank's ability to meet obligations.")
]

# ====================== CREATE ALL PDFs ======================
topics = [
    ("Python", python_qna, "Python_Interview_Questions.pdf"),
    ("Java", java_qna, "Java_Interview_Questions.pdf"),
    ("SQL", sql_qna, "SQL_Interview_Questions.pdf"),
    ("C", c_qna, "C_Interview_Questions.pdf"),
    ("C++", cpp_qna, "C++_Interview_Questions.pdf"),
    ("Django", django_qna, "Django_Interview_Questions.pdf"),
    ("MongoDB", mongodb_qna, "MongoDB_Interview_Questions.pdf"),
    ("Banking", banking_qna, "Banking_Interview_Questions.pdf")
]

for topic, qna, filename in topics:
    create_pdf(topic, qna, filename)
