## Game:  ✈️ Broiler747

## Description
A single-player flight simulation game where players manage fuel, weather, and distance to reach destinations.
Combines real-world airport data (from the course database) with eco-conscious gameplay.
Goal: Reach your destination while minimizing fuel use and emissions — promoting awareness of sustainable aviation.

## Installation
For this project to function properly, use modified_db.sql . It contains modified tables from original database, so usage of this file is required if you possess original database (lp.sql contains this data. This file is not present here). Otherwise, run this modified_db.sql file in your IDE (DataGrip for example) or specified programs like HeidiSQL or MySQL Workbench.

## Controls
Controls are made by using arrows keys: Up and Down

## Booting process:
*  Run the server: backend/app.py
*  Entry point: frontend/views/main_menu.html

**Project Overview**
--------------------

*   **Core Gameplay:**
    
    *   Plane moves from left to right, avoiding obstacles. Player controls only up/down movement 
    *   Game ends either when plane hits an obsatcle **or** it reaches the destination (ending_airport).
    *   Score increases with survival and answered quiz.
        
*   **Additional Mechanic:**
    
    *   Quiz questions pop up after the main gameplay loop in the results main menu 
    *   Correct answers give bonus points at the end of the session.
    *   This encourages learning/fun interactions.
        
*   **Architecture:** MVC pattern:
    
    *   **Models:**
        
        *   Plane, Obstacle, GameState → core gameplay objects.
        *   Player, Quiz, Game → persistent player data and score.
            
    *   **Controller:**
        
        *   Game loop (gameplay.js) → handles input, collisions.  
        *   Menu system (main_menu, choose_player, new_player, statistics) → start/pause menus, player selection, statistics.
            
    *   **View:**
        
        *   Pixel art style and images taken for studies purposes.
            
*   **Persistence:**

    *  MariaDB via REST API for longer-term persistence (Flask endpoints).

### **Game Session Flow (simplified)**

1.  **Menu:** Player chooses or creates profile. Further chooses route from start to finishing airport (routes are divided by distance, so that creates difficulty)
    
2.  **Game starts:**
    
    *   In the game, user moves plane and obstacles, each frame we track where obsatcles and user is located inside of the window.   
    *   Checks for crashes.     
    *   Score increments continuously.
        
3.  **Game ends:**
    
    *   Either plane crashes, by coliding with obstacle ones
    *   Or destination reached 
    *   Quiz triggers after flight during the results menu. So it is up to the player to take his/her knowledge to the test
        
4.  **Results:**
    
    *   Score + bonus points from quizzes.
    *   Player totals updated and kept in MariaDB DataBase by transfering via API calls from frontend→backend→DB and shown in statisics page by query