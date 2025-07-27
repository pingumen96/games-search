# Architecture Diagram - Games Database Refactored

## Class Diagram Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              GAMES DATABASE ARCHITECTURE                        │
│                                 (Refactored Version)                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   main_refactored.py      │                 │                 │         │
│                 │         │  GameController │                 │         │
│     main()      │────────▶│    (Facade)     │◄────────────────│         │
│                 │         │                 │                 │         │
└─────────────────┘         └─────────────────┘                 │         │
                                     │                          │         │
                                     │                          │         │
┌─────────────────┐                  │                          │         │
│   ConsoleUI     │                  │                          │         │
│ (Template Method)│◄─────────────────┘                          │         │
│                 │                                             │         │
│  + run()        │                                             │         │
│  + show_menu()  │                                             │         │
│  + initialize() │                                             │         │
└─────────────────┘                                             │         │
         │                                                      │         │
         │ extends                                              │         │
         ▼                                                      │         │
┌─────────────────┐                                             │         │
│     BaseUI      │                                             │         │
│   (Abstract)    │                                             │         │
│                 │                                             │         │
└─────────────────┘                                             │         │

┌─────────────────────────────────────────────────────────────────┐       │
│                        SERVICES LAYER                          │       │
└─────────────────────────────────────────────────────────────────┘       │
                                                                          │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐       │
│  GameAPIService │    │ AIReviewService │    │   RAWGService   │       │
│   (Abstract)    │    │   (Abstract)    │    │                 │       │
│                 │    │                 │    │ + fetch_games() │       │
│+ fetch_games()  │    │+ generate_review│    │                 │       │
└─────────────────┘    │+ is_available() │    └─────────────────┘       │
         ▲              └─────────────────┘             │                │
         │                       ▲                     │                │
         │                       │                     │ implements     │
         │                       │                     ▼                │
         │              ┌─────────────────┐    ┌─────────────────┐       │
         │              │OpenAIReviewService   │                 │       │
         │              │                 │    │                 │       │
         │              │+ generate_review│    │                 │       │
         │              │+ is_available() │    │                 │       │
         │              └─────────────────┘    │                 │       │
         │                                     │                 │       │
         └─────────────────────────────────────┼─────────────────┘       │
                                               │                         │
                                               │                         │
┌─────────────────────────────────────────────────────────────────────────┤
│                        MODELS LAYER                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                               │
┌─────────────────┐                           │
│      Game       │◄──────────────────────────┘
│   (Data Model)  │
│                 │
│+ title: str     │
│+ platforms: List│
│+ release_date   │
│+ genres: List   │
│+ ai_review      │
│+ ai_rating      │
│                 │
│+ to_dict()      │
│+ matches_filter()│
└─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              EXPORTERS LAYER                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  ExportManager  │────────▶│ExportStrategyFactory  │──▶│ ExportStrategy  │
│                 │         │                 │         │   (Abstract)    │
│+ export_games() │         │+ create_strategy│         │                 │
│+ get_formats()  │         │+ get_formats()  │         │+ export()       │
└─────────────────┘         └─────────────────┘         │+ extension      │
                                     │                   │+ is_available   │
                                     │                   └─────────────────┘
                                     │                            ▲
                                     ▼                            │
                    ┌─────────────────────────────────────────────┤
                    │            CONCRETE STRATEGIES              │
                    └─────────────────────────────────────────────┘
                                     │
          ┌─────────────┬────────────┼────────────┬─────────────┐
          │             │            │            │             │
          ▼             ▼            ▼            ▼             ▼
┌─────────────────┐┌─────────────────┐┌─────────────────┐┌─────────────────┐
│ CSVExportStrategy││MarkdownExport  ││ XLSXExportStrategy││ XMLExportStrategy│
│                 ││   Strategy      ││                 ││                 │
│+ export()       ││                 ││+ export()       ││+ export()       │
│+ extension=".csv││+ export()       ││+ extension=".xlsx││+ extension=".xml│
│+ is_available=T ││+ extension=".md"││+ is_available() ││+ is_available=T │
└─────────────────┘│+ is_available=T │└─────────────────┘└─────────────────┘
                   └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            CONFIGURATION LAYER                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│     Config      │
│   (Singleton)   │
│                 │
│+ rawg_api_key   │
│+ openai_api_key │
│+ has_openai_key │
│                 │
│- _instance      │
│- _initialized   │
└─────────────────┘
```

## Design Patterns Used

### 1. **Singleton Pattern** - `Config`
- Ensures single instance of configuration
- Global access point for settings
- Lazy initialization

### 2. **Facade Pattern** - `GameController`
- Provides simplified interface to complex subsystem
- Coordinates between services, models, and exporters
- Hides implementation details from UI

### 3. **Strategy Pattern** - `ExportStrategy`
- Encapsulates export algorithms
- Runtime algorithm selection
- Easy addition of new export formats

### 4. **Factory Pattern** - `ExportStrategyFactory`
- Creates export strategy objects
- Centralizes object creation logic
- Supports plugin-like architecture

### 5. **Template Method Pattern** - `BaseUI`
- Defines skeleton of UI workflow
- Subclasses implement specific steps
- Promotes code reuse

### 6. **Abstract Factory Pattern** - Services
- Family of related objects (API services)
- Interchangeable implementations
- Consistent interfaces

## Data Flow

```
User Input (UI) → GameController (Facade) → Services (API/AI) → Models (Game) → Exporters (Strategy) → File Output
     ▲                    │                        │                │                    │
     │                    ▼                        ▼                ▼                    ▼
     └────────── Display Results ◄──── Business Logic ◄──── Data Processing ◄── Format Selection
```

## Benefits of This Architecture

### 1. **Separation of Concerns**
- Each layer has distinct responsibility
- UI separated from business logic
- Data model independent of persistence

### 2. **Loose Coupling**
- Components interact through interfaces
- Easy to replace implementations
- Changes in one layer don't affect others

### 3. **High Cohesion**
- Related functionality grouped together
- Clear module boundaries
- Single responsibility principle

### 4. **Extensibility**
- New export formats via Strategy pattern
- New AI services via interface implementation
- New UI types via Template Method

### 5. **Testability**
- Each component can be unit tested
- Mock objects easily created
- Dependencies can be injected

## SOLID Principles Applied

### **S** - Single Responsibility Principle
- `Game`: Only data model responsibilities
- `RAWGService`: Only API communication
- `ExportManager`: Only export coordination

### **O** - Open/Closed Principle
- Open for extension (new strategies, services)
- Closed for modification (existing code unchanged)

### **L** - Liskov Substitution Principle
- All export strategies interchangeable
- All AI services interchangeable
- Subclasses can replace base classes

### **I** - Interface Segregation Principle
- `GameAPIService` and `AIReviewService` separate
- Clients depend only on needed interfaces
- No forced unused method implementations

### **D** - Dependency Inversion Principle
- High-level modules depend on abstractions
- Controllers use interfaces, not concrete classes
- Dependency injection enables flexibility
