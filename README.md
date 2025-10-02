## Game:  ✈️ Broiler747

## 📄 Description
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

## ⚙️ Installation
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut enim ad minim veniam.

## 🎮 Controls
Lorem ipsum dolor sit amet.

## Let me do the thing!


**Project Overview**
--------------------

*   **Core Gameplay:**
    
    *   Plane moves from left to right, avoiding obstacles. Player controls only up/down movement 
    *   Game ends either when plane health ≤ 0 **or** it reaches the destination (airport).
    *   Score increases with survival and possibly distance traveled.
        
*   **Additional Mechanic:**
    
    *   Quiz questions pop up during gameplay (on top of the console “view”).
    *   Correct answers give bonus points at the end of the session.
    *   This encourages learning/fun interactions.
        
*   **Architecture:** MVC pattern:
    
    *   **Models:**
        
        *   Plane, Obstacle, World, GameState → core gameplay objects.
        *   Player, Quiz, Achievement → persistent player data and rewards.
            
    *   **Controller:**
        
        *   Game loop (GameController) → updates world, handles input, collisions.  
        *   Menu system (MenuController) → start/pause menus, player selection.
            
    *   **View:**
        
        *   Temporary console graphics (ASCII or simple text-based representation).
        *   Later could be replaced by a graphical UI or during this implementation using simple JS and HTML.
            
*   **Persistence:**
    
    *   JSON file acts as lightweight storage (avoiding constant MySQL calls).
    *   Optional: MySQL via REST API for longer-term persistence (Flask endpoints).

### **Game Session Flow (simplified)**

1.  **Menu:** Player chooses or creates profile.
    
2.  **Game starts:**
    
    *   World.update() moves plane and obstacles each tick.   
    *   World.check\_collisions() checks for crashes.   
    *   ask\_quiz() triggers occasionally during flight.  
    *   Score increments continuously.
        
3.  **Game ends:**
    
    *   Either plane crashes (health ≤ 0) 
    *   Or destination reached (x ≥ destination\_x)
        
4.  **Results:**
    
    *   Score + bonus points from quizzes.
    *   Achievements checked/unlocked.
    *   Player totals updated in JSON/MySQL via DB functions or API.