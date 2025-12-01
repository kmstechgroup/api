# Diagrama de Modelos - SafeOn API

## Estructura de Modelos con AbstractUser

```mermaid
erDiagram
    %% Django AbstractUser (Base)
    AbstractUser {
        int id PK
        string username
        string first_name
        string last_name
        string email
        string password
        boolean is_active
        boolean is_staff
        boolean is_superuser
        datetime date_joined
        datetime last_login
    }

    %% User Model (extends AbstractUser)
    User {
        uuid id PK "UUID primary key"
        string email UK "Unique email"
        string username "Optional username"
        string google_id UK "Google OAuth ID"
        boolean is_oauth_user "OAuth user flag"
        bigint identificator "DNI/Passport"
        string address "User address"
        string blood_type "A+, A-, B+, etc."
        string sex "M, F, X"
        int height "Height in cm"
        int weight "Weight in kg"
        int age "User age"
        text allergies_other "Custom allergies"
        text chronic_diseases_other "Custom diseases"
        text previous_surgeries_other "Custom surgeries"
        text disabilities_other "Custom disabilities"
        json close_contacts "Emergency contacts"
        bigint phone_number "Phone number"
        int strikes "Warning count"
        boolean blocked "Blocked status"
        datetime updated_at "Last update"
    }

    %% Medical Information Models
    Allergy {
        int id PK
        string name UK "Allergy name"
        boolean is_active "Active status"
        datetime created_at "Creation date"
    }

    ChronicDisease {
        int id PK
        string name UK "Disease name"
        boolean is_active "Active status"
        datetime created_at "Creation date"
    }

    PreviousSurgery {
        int id PK
        string name UK "Surgery name"
        boolean is_active "Active status"
        datetime created_at "Creation date"
    }

    Disability {
        int id PK
        string name UK "Disability name"
        boolean is_active "Active status"
        datetime created_at "Creation date"
    }

    %% Department Model
    Department {
        string code_department PK "Auto-generated code"
        string type_department "F=Firefighters, P=Police"
        string name_department "Department name"
        json jurisdiction "Coverage area"
        float city_center_lat "Latitude"
        float city_center_lon "Longitude"
        bigint phone "Department phone"
    }

    %% Emergency Model
    Emergency {
        int code_emergency PK "Auto-increment"
        datetime date_time "Creation timestamp"
        float latitude "Emergency location"
        float longitude "Emergency location"
        uuid created_by FK "User who created"
        int emergency_main FK "Parent emergency"
    }

    %% Junction Table
    CommunicateEmergencyDepartment {
        string code_department FK
        int code_emergency FK
        boolean is_close "Department response status"
    }

    %% Relationships
    AbstractUser ||--o{ User : "extends"
    
    User ||--o{ Allergy : "many-to-many"
    User ||--o{ ChronicDisease : "many-to-many"
    User ||--o{ PreviousSurgery : "many-to-many"
    User ||--o{ Disability : "many-to-many"
    
    User ||--o{ Emergency : "creates"
    Emergency ||--o{ Emergency : "self-referential"
    
    Department ||--o{ CommunicateEmergencyDepartment : "participates"
    Emergency ||--o{ CommunicateEmergencyDepartment : "involves"
    
    Department ||--o{ Emergency : "many-to-many through junction"
```

## Explicación de la Estructura

### 1. **AbstractUser (Base de Django)**
- Modelo base de Django que proporciona funcionalidades de autenticación
- Incluye campos estándar como username, email, password, etc.
- Proporciona métodos de autenticación y permisos

### 2. **User (Modelo Personalizado)**
- **Hereda de AbstractUser**: Extiende todas las funcionalidades base
- **UUID como PK**: Usa UUID en lugar del ID entero por defecto
- **OAuth Integration**: Soporte para Google OAuth con `google_id` e `is_oauth_user`
- **Información Médica**: Campos para tipo de sangre, altura, peso, edad
- **Relaciones Many-to-Many**: Con modelos predefinidos de información médica
- **Campos Personalizados**: Para información médica no predefinida
- **Sistema de Advertencias**: Campo `strikes` y `blocked` para gestión de usuarios

### 3. **Modelos de Información Médica**
- **Allergy, ChronicDisease, PreviousSurgery, Disability**: Modelos predefinidos
- **Relación Many-to-Many**: Con el modelo User para flexibilidad
- **Campos "other"**: En User para información médica personalizada

### 4. **Department**
- **Código Auto-generado**: Basado en tipo (F/P) + número secuencial
- **Tipos**: Bomberos (F) y Policía (P)
- **Ubicación**: Coordenadas del centro de la ciudad
- **Jurisdicción**: Área de cobertura en formato JSON

### 5. **Emergency**
- **Auto-increment PK**: Código de emergencia único
- **Ubicación**: Latitud y longitud de la emergencia
- **Creador**: Referencia al User que creó la emergencia
- **Jerarquía**: Auto-referencia para emergencias relacionadas
- **Departamentos**: Relación many-to-many a través de tabla intermedia

### 6. **CommunicateEmergencyDepartment (Tabla Intermedia)**
- **Junction Table**: Para la relación many-to-many entre Emergency y Department
- **Estado de Respuesta**: Campo `is_close` para indicar si el departamento respondió

## Características Clave

1. **Herencia de AbstractUser**: El modelo User mantiene toda la funcionalidad de autenticación de Django
2. **Flexibilidad Médica**: Sistema híbrido con opciones predefinidas y campos personalizados
3. **OAuth Ready**: Preparado para autenticación con Google
4. **Sistema de Emergencias**: Estructura jerárquica con auto-referencias
5. **Gestión de Departamentos**: Sistema de códigos auto-generados y jurisdicciones
6. **Auditoría**: Campos de timestamp para seguimiento de cambios


