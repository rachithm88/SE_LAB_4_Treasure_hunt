# SE_LAB_4_Treasure_hunt
Exploring a new and updated procedurally generated dungeon, collection of the key, then open the chest.

# Treasure Hunt — Enhanced Edition

An expanded Pygame-based dungeon crawler featuring procedural exploration, trap hazards, patrolling enemy guards, real-time mini-map tracking, and a dynamic HUD inventory.

---

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **W / A / S / D** or **Arrow Keys** | Move character |
| **R** | Restart game / Reset run |

---

## ✨ Features Implemented (Lab 4)

### 1. 🩸 Floor Traps
* Red floor tiles are scattered across key corridors.
* Stepping on a trap instantly resets the player back to the starting position and alerts them via an on-screen status message.

### 2. 🛡️ Patrolling Enemy Guard
* An enemy guard continuously patrols back and forth in the corridor leading to the treasure chest.
* Colliding with the guard resets the player to the starting room.

### 3. 🗺️ Real-Time Mini-Map
* A compact mini-map is rendered in the top-right corner of the HUD.
* Distinguishes dungeon walls from floor paths and tracks the player's position in real time using a bright cyan marker.

### 4. 🎒 Dynamic Inventory UI Slot
* A dedicated HUD inventory slot is rendered in the bottom-left corner of the screen.
* Displays an empty slot at the start and dynamically renders a gold key icon immediately upon key collection.

---

## 🕹️ Objective & How to Play

1. Navigate through the dungeon while avoiding red floor traps and the patrolling guard.
2. Locate and pick up the **Gold Key** (updates your HUD inventory slot).
3. Reach the **Treasure Chest** at the end of the dungeon to unlock it and win!
4. Press **R** at any point to restart your run.

---

## 📁 Repository Structure

```text
├── game_updated.py           # Main Pygame source file with updated features
├── README.md                 # Project documentation
├── before_changes.mp4        # baseline gameplay recording
├── after_changes.mp4         # completed feature showcase video
└── chat_history.pdf          # Complete LLM conversation export
