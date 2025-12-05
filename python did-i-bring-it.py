import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. CONFIGURE STREAMLIT PAGE
# ==========================================
st.set_page_config(
    page_title="Did I Bring It?",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 0rem;
                padding-right: 0rem;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# 2. APP CONTENT
# ==========================================
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Did I Bring It?</title>
    
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='12' fill='%232A4298'/%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z' fill='white'/%3E%3C/svg%3E">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    
    <style>
        :root {
            --bg-color: #E0F8FF;
            --primary-blue: #2A4298;
            --accent-blue: #A8C0FF;
            --text-dark: #1a1a1a;
            --button-blue: #B0C4F8;
            --font-poppins: 'Poppins', sans-serif;
            --danger-color: #e53935;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background-color: #262730; 
            font-family: var(--font-poppins);
            height: 100vh;
            width: 100vw;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            margin: 0;
        }

        /* --- RESPONSIVE MOBILE VIEWPORT --- */
        #mobile-viewport {
            width: 100%;
            height: 100%;
            /* Simulate a large phone on desktop, fill on mobile */
            max-width: 420px; 
            max-height: 90vh; /* Fits nicely in browser window */
            background-color: var(--bg-color);
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 50px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            border-radius: 20px;
        }
        
        /* Actual Mobile Devices: Full Screen, No Radius/Shadow */
        @media (max-width: 480px) {
            #mobile-viewport { 
                max-width: 100%; 
                max-height: 100%; 
                border-radius: 0; 
                box-shadow: none;
            }
        }

        /* --- SCREEN LAYOUT --- */
        .screen {
            display: none; 
            flex-direction: column;
            width: 100%; 
            height: 100%;
            background-color: var(--bg-color);
            animation: fadeIn 0.3s ease-in-out;
        }
        .screen.active { display: flex; }

        /* HEADER (Fixed Top) */
        .app-bar { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 20px; 
            flex-shrink: 0; 
            background: transparent;
            z-index: 10;
            min-height: 70px;
        }
        .app-bar h2 { font-size: 1.25rem; font-weight: 600; color: #000; letter-spacing: 0.5px; }
        .icon-btn { background: none; border: none; font-size: 1rem; display: flex; align-items: center; cursor: pointer; color: var(--text-dark); }

        /* SCROLLABLE AREA (Middle) */
        .scrollable-content {
            flex-grow: 1;
            overflow-y: auto;
            width: 100%;
            padding: 0 20px 20px 20px; /* Side padding inside scroll area */
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .scrollable-content::-webkit-scrollbar { display: none; }

        /* CONTENT UTILS */
        .content-center { display: flex; flex-direction: column; align-items: center; width: 100%; }
        .input-group { width: 100%; display: flex; justify-content: center; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- COMPONENTS --- */

        /* Calendar */
        .calendar-card { 
            background: #fff; 
            width: 100%;
            border-radius: 25px; 
            padding: 20px; 
            box-shadow: 0 8px 20px rgba(0,0,0,0.05); 
            margin-bottom: 20px;
            margin-top: 10px;
            flex-shrink: 0;
        }
        .calendar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .calendar-days, .calendar-grid-header { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; text-align: center; margin-bottom: 15px; }
        .day { font-size: 1rem; display: flex; justify-content: center; align-items: center; border-radius: 50%; aspect-ratio: 1 / 1; width: 100%; cursor: pointer; }
        .has-event { background-color: #E3F2FD; color: var(--primary-blue); font-weight: 700; position: relative; }
        .has-event::after { content: ''; position: absolute; bottom: 5px; width: 4px; height: 4px; background: var(--primary-blue); border-radius: 50%; }
        .today-marker { border: 2px solid var(--primary-blue); color: var(--primary-blue); font-weight: bold; }
        .day-name { font-size: 0.75rem; color: #bbb; font-weight: 600; }
        .time-row { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f0f0f0; padding-top: 15px; width: 100%; }
        .chip-gray { background: #eee; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; }

        /* Reminders Section */
        .reminders-section { width: 100%; margin-bottom: 20px; }
        .reminders-section h4 { margin: 0 0 15px 5px; font-size: 1.1rem; font-weight: 600; text-align: left; }
        
        .reminder-card { 
            background: rgba(255, 255, 255, 0.7); border: 2px solid #fff; border-radius: 25px; 
            padding: 10px 15px; display: flex; align-items: center; margin-bottom: 12px; height: 70px; 
            cursor: pointer; box-shadow: 0 2px 10px rgba(0,0,0,0.02); width: 100%;
        }
        .rem-title { font-weight: 600; margin-right: auto; margin-left: 10px; color: var(--text-dark); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .rem-date, .rem-time { background: #CFD8DC; padding: 5px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 500; margin-left: 5px; white-space: nowrap; flex-shrink: 0;}

        /* Icons */
        .icon-box { width: 45px; height: 45px; border-radius: 50%; display: flex; justify-content: center; align-items: center; flex-shrink: 0; }
        .icon-box span { color: white; font-size: 24px; }
        .profile-icon-mini { width: 45px !important; height: 45px !important; border-radius: 50%; background: #87CEEB; overflow: hidden; cursor: pointer; border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); flex-shrink: 0; }
        .profile-icon-mini img { width: 100%; height: 100%; object-fit: cover; display: block; }

        /* Avatars */
        .avatar-large, .avatar-large-circle { width: 130px !important; height: 130px !important; min-width: 130px; min-height: 130px; background-color: #fff; border-radius: 50%; overflow: hidden; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .avatar-large-circle { background-color: #6495ED; display: flex; justify-content: center; align-items: flex-end; }
        .avatar-large img, .avatar-large-circle img { width: 100%; height: 100%; object-fit: cover; }
        .avatar-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; width: 100%; justify-items: center; }
        .avatar-option { width: 70px; height: 70px; border-radius: 50%; background-color: #ddd; overflow: hidden; border: 3px solid transparent; cursor: pointer; }
        .avatar-option.selected { border-color: #fff; box-shadow: 0 0 0 3px var(--primary-blue); }
        .avatar-option img { width: 100%; height: 100%; object-fit: cover; }

        /* Lists & Trash */
        .list-container { width: 100%; display: flex; flex-direction: column; }
        .list-item { background: #D4F1F4; border: 1px solid #7F8C8D; border-radius: 20px; padding: 15px; display: flex; align-items: center; margin-bottom: 15px; cursor: pointer; width: 100%; }
        .list-text { font-weight: 600; flex-grow: 1; margin-left: 15px; }
        
        .trash-container { 
            display: flex; justify-content: center; align-items: center;
            padding: 20px; transition: transform 0.2s; margin-bottom: 10px; margin-top: auto; flex-shrink: 0;
        }
        .trash-container.trash-hover { transform: scale(1.3); }
        .trash-icon { font-size: 35px; color: #aaa; transition: color 0.3s; }
        .trash-container.trash-hover .trash-icon { color: #ff5252; }
        .hint-text { text-align: center; color: #888; font-size: 0.8rem; margin-top: 10px; flex-shrink: 0; width: 100%; display: block; }

        /* Forms */
        .form-container { width: 100%; max-width: 340px; display: flex; flex-direction: column; gap: 15px; }
        .form-container label { font-size: 0.95rem; font-weight: 500; color: #444; display: block; margin-bottom: 5px; margin-top: 5px; text-align: left; width: 100%; }
        .input-field { width: 100%; padding: 12px 15px; border-radius: 12px; border: 1px solid #ccc; background: #fff; font-size: 1rem; outline: none; font-family: var(--font-poppins); }
        .underline-input { background: transparent; border: none; border-bottom: 2px solid var(--text-dark); text-align: center; font-size: 1.5rem; padding: 10px; width: 80%; margin-bottom: 30px; outline: none; font-weight: 500; }

        /* Category Grid */
        .category-label { font-size: 0.9rem; font-weight: 500; color: #666; margin-bottom: 5px; align-self: flex-start; margin-left: 5px; }
        .category-grid { display: flex; gap: 12px; overflow-x: auto; padding: 10px 5px; width: 100%; margin-bottom: 10px; scrollbar-width: none; }
        .category-grid::-webkit-scrollbar { display: none; }
        .category-option { width: 55px; height: 55px; border-radius: 50%; display: flex; justify-content: center; align-items: center; cursor: pointer; flex-shrink: 0; border: 2px solid transparent; transition: transform 0.2s, box-shadow 0.2s; }
        .category-option.selected { border-color: #2A4298; transform: scale(1.1); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .category-option span { color: white; font-size: 26px; }

        /* Colors */
        .bg-purple { background: #D1C4E9; } .bg-purple span { color: #5E35B1; }
        .bg-orange { background: #FFE0B2; } .bg-orange span { color: #FB8C00; }
        .bg-green { background: #C8E6C9; } .bg-green span { color: #43A047; }
        .bg-blue { background: #BBDEFB; } .bg-blue span { color: #1976D2; }
        .bg-gray { background: #90A4AE; } .bg-gray span { color: #37474F; }
        .bg-red { background: #ffcdd2; } .bg-red span { color: #c62828; }
        .bg-teal { background: #b2dfdb; } .bg-teal span { color: #00695c; }

        /* Buttons & Other */
        .button-row { display: flex; gap: 20px; justify-content: center; width: 100%; margin-top: 30px; margin-bottom: 30px; flex-shrink: 0; }
        .btn-primary { background-color: var(--button-blue); padding: 12px 30px; border-radius: 12px; border: none; cursor: pointer; font-weight: 600; font-size: 1rem; width: 130px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .btn-secondary { background-color: #fff; padding: 12px 30px; border-radius: 12px; border: none; cursor: pointer; font-weight: 500; font-size: 1rem; width: 130px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .btn-icon-small { background: var(--primary-blue); color: white; border: none; border-radius: 8px; width: 50px; cursor: pointer; display: flex; justify-content: center; align-items: center; flex-shrink: 0; }
        .btn-text-danger { margin-top: 10px; color: var(--danger-color); background: none; border: none; font-weight: 600; cursor: pointer; font-size: 0.9rem; }
        .btn-done-pill { margin-top: 30px; background: #D1C4E9; width: 150px; padding: 15px; border: none; border-radius: 30px; font-size: 1.1rem; font-weight: 600; display: block; margin-left: auto; margin-right: auto; cursor: pointer; }

        /* User Switcher */
        .switch-accounts-section { width: 100%; background: rgba(255,255,255,0.6); padding: 15px; border-radius: 20px; margin-top: 10px; text-align: center; }
        .users-row { display: flex; justify-content: center; gap: 15px; margin-top: 10px; flex-wrap: wrap; }
        .small-user-avatar { width: 50px; height: 50px; border-radius: 50%; overflow: hidden; cursor: grab; border: 2px solid transparent; }
        .small-user-avatar.active-user { border-color: var(--primary-blue); box-shadow: 0 0 10px rgba(42, 66, 152, 0.3); }
        .small-user-avatar img { width: 100%; height: 100%; object-fit: cover; pointer-events: none; }

        /* Checklist Items */
        .checklist-content { padding: 20px 40px; width: 100%; }
        .big-title { font-size: 2.5rem; font-weight: 600; margin-bottom: 10px; }
        .tags-row { display: flex; gap: 10px; margin-bottom: 40px; }
        .tag { background: #CFD8DC; padding: 5px 15px; border-radius: 15px; font-size: 0.9rem; font-weight: 500; }
        .checkbox-container { display: flex; align-items: center; position: relative; padding-left: 40px; cursor: pointer; font-size: 1.2rem; font-weight: 500; margin-bottom: 20px; width: 100%; }
        .checkbox-container input { position: absolute; opacity: 0; }
        .checkmark-box { position: absolute; left: 0; height: 26px; width: 26px; border: 2px solid var(--text-dark); border-radius: 6px; }
        .checkbox-container input:checked ~ .checkmark-box { background-color: var(--primary-blue); border-color: var(--primary-blue); }
        .checkbox-container input:checked ~ .checkmark-box:after { display: block; }
        .checkmark-box:after { content: ""; position: absolute; display: none; left: 8px; top: 4px; width: 6px; height: 12px; border: solid white; border-width: 0 3px 3px 0; transform: rotate(45deg); }
        .delete-item-icon { color: var(--danger-color); font-size: 1.5rem; cursor: pointer; }
        .add-item-row { display: flex; gap: 10px; width: 100%; }
        .temp-tag { background: #fff; padding: 5px 10px; border-radius: 15px; font-size: 0.9rem; display: flex; align-items: center; gap: 5px; border: 1px solid #ccc; margin-right: 5px; margin-bottom: 5px; }
        .temp-tags-container { display: flex; flex-wrap: wrap; margin-top: 10px; width: 100%; }

        /* Splash */
        #splash-screen { background-color: #2A4298; z-index: 9999; display: flex; align-items: center; justify-content: center; position: absolute; top:0; left:0; width: 100%; height: 100%; }
        .union-logo { width: 100px; height: 100px; border: 2px solid #879BF0; border-radius: 50% 0 50% 0; display: flex; justify-content: center; align-items: center; margin-bottom: 20px; transform: rotate(-45deg); box-shadow: 0 0 20px rgba(135, 155, 240, 0.5); }
        .union-logo .checkmark { font-size: 60px; color: #879BF0; transform: rotate(45deg); }
        .logo-container { display: flex; flex-direction: column; align-items: center; color: white; }
        .logo-container h1 { font-weight: 300; letter-spacing: 3px; font-size: 1.5rem; }
    </style>
</head>
<body>

<div id="mobile-viewport">

    <!-- SCREEN 1: SPLASH SCREEN -->
    <div id="splash-screen" class="screen active">
        <div class="logo-container">
            <div class="union-logo">
                <span class="material-icons-round checkmark">check</span>
            </div>
            <h1>DID I BRING IT?</h1>
        </div>
    </div>

    <!-- SCREEN 2: ADD / EDIT USER SCREEN -->
    <div id="add-user-screen" class="screen">
        <div class="app-bar">
            <button class="icon-btn" id="user-back-btn" onclick="navigateTo('home-screen')"><span class="material-icons-round">arrow_back_ios</span></button>
            <h2 id="user-screen-title" style="flex-grow:1; text-align:center; margin-right: 24px;">Add New User</h2>
        </div>
        
        <div class="scrollable-content">
            <div class="content-center">
                <div class="avatar-large-wrapper">
                    <div class="avatar-large">
                        <img id="setup-main-avatar" src="" alt="Avatar">
                    </div>
                </div>
                
                <div class="input-group">
                    <input type="text" id="username-input" placeholder="Enter Name" class="underline-input">
                </div>

                <div class="avatar-grid" id="setup-avatar-grid"></div>
                
                <div class="button-row">
                    <button class="btn-primary" onclick="saveUser()">Done</button>
                    <button class="btn-secondary" onclick="cancelUserAction()">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <!-- SCREEN 3: PROFILE SCREEN -->
    <div id="profile-screen" class="screen">
        <div class="app-bar">
            <button class="icon-btn" onclick="navigateTo('home-screen')"><span class="material-icons-round">arrow_back_ios</span></button>
            <h2>Profile</h2>
            <button class="icon-btn" onclick="startAddUserFlow()"><span class="material-icons-round">person_add</span></button>
        </div>
        
        <div class="scrollable-content">
            <div class="content-center">
                <div class="avatar-large-circle">
                    <img id="profile-main-avatar" src="" alt="User">
                </div>
                
                <h2 id="profile-display-name">User</h2>

                <div class="switch-accounts-section">
                    <p>Switch Accounts:</p>
                    <div id="other-users-list" class="users-row"></div>
                </div>

                <div class="button-row" style="margin-top: 30px;">
                    <button class="btn-primary" onclick="startEditUserFlow()">Edit Profile</button>
                    <button class="btn-secondary" onclick="navigateTo('home-screen')">Back</button>
                </div>
            </div>
        </div>

        <p class="hint-text">Drag avatar here to delete user</p>
        <div class="trash-container" id="profile-trash-target">
            <span class="material-icons-round trash-icon">delete_outline</span>
        </div>
    </div>

    <!-- SCREEN 4: HOME SCREEN -->
    <div id="home-screen" class="screen">
        <div class="app-bar home-header">
            <button class="icon-btn" onclick="navigateTo('lists-screen')"><span class="material-icons-round" style="font-size: 36px;">menu</span></button>
            <div class="profile-icon-mini" onclick="navigateTo('profile-screen')">
                <img id="home-avatar-img" src="" alt="User">
            </div>
        </div>

        <div class="scrollable-content">
            <div class="calendar-card">
                <div class="calendar-header">
                    <h3 id="calendar-month-year">Loading...</h3> 
                    <div class="calendar-nav">
                        <span class="material-icons-round" onclick="changeMonth(-1)">chevron_left</span>
                        <span class="material-icons-round" onclick="changeMonth(1)">chevron_right</span>
                    </div>
                </div>
                <div class="calendar-grid-header">
                    <div class="day-name">SUN</div><div class="day-name">MON</div><div class="day-name">TUE</div><div class="day-name">WED</div><div class="day-name">THU</div><div class="day-name">FRI</div><div class="day-name">SAT</div>
                </div>
                <div class="calendar-days" id="calendar-days-grid"></div>

                <div class="time-row">
                    <span style="font-weight: 500; color: #555;">Time</span>
                    <span class="chip-gray" id="current-time-display">--:--</span>
                </div>
            </div>

            <div class="reminders-section">
                <h4>Reminders:</h4>
                <div id="home-reminders-list"></div>
            </div>
        </div>
    </div>

    <!-- SCREEN 5: LISTS VIEW -->
    <div id="lists-screen" class="screen">
        <div class="app-bar">
            <button class="icon-btn" onclick="navigateTo('home-screen')"><span class="material-icons-round">arrow_back_ios</span> Home</button>
            <h2 style="flex-grow: 1; text-align: center; margin-right: 60px;">Lists</h2>
            <button class="icon-btn" onclick="navigateTo('add-list-screen')"><span class="material-icons-round" style="font-size: 28px;">add</span></button>
        </div>

        <div class="scrollable-content" style="padding: 0;">
            <div class="list-container" id="all-lists-container" style="padding: 20px;"></div>
        </div>

        <p class="hint-text">Drag a list to the trash to delete</p>
        <div class="trash-container" id="trash-target">
            <span class="material-icons-round trash-icon">delete_outline</span>
        </div>
    </div>

    <!-- SCREEN 6: CHECKLIST DETAILS -->
    <div id="checklist-screen" class="screen">
        <div class="app-bar">
            <button class="icon-btn" onclick="navigateTo('lists-screen')"><span class="material-icons-round">arrow_back_ios</span></button>
            <h2>Checklist</h2>
            <button class="icon-btn" onclick="toggleEditChecklistMode()"><span class="material-icons-round" id="cl-edit-icon">edit</span></button>
        </div>
        
        <div class="scrollable-content">
            <div id="cl-view-header">
                <h1 class="big-title" id="cl-title">Title</h1>
                <div class="tags-row">
                    <span class="tag" id="cl-date">Date</span>
                    <span class="tag" id="cl-time">Time</span>
                </div>
            </div>

            <div id="cl-edit-header" style="display: none; margin-bottom: 20px;">
                <input type="text" id="edit-cl-title" class="input-field" placeholder="Title">
                <div style="display: flex; gap: 10px;">
                    <input type="date" id="edit-cl-date" class="input-field">
                    <input type="time" id="edit-cl-time" class="input-field">
                </div>
                <div class="add-item-row" style="margin-top: 10px;">
                    <input type="text" id="add-cl-item-input" class="input-field" placeholder="Add new item...">
                    <button class="btn-icon-small" onclick="addChecklistItemInEdit()"><span class="material-icons-round">add</span></button>
                </div>
            </div>

            <div class="check-group" id="cl-items-container"></div>
            
            <div class="button-row">
                <button id="cl-action-btn" class="btn-done-pill" onclick="navigateTo('home-screen')">Done</button>
            </div>
        </div>
    </div>

    <!-- SCREEN 7: ADD NEW LIST FORM -->
    <div id="add-list-screen" class="screen">
        <div class="app-bar">
            <button class="icon-btn" onclick="navigateTo('lists-screen')"><span class="material-icons-round">arrow_back_ios</span> Cancel</button>
            <h2>New List</h2>
            <div style="width: 24px;"></div>
        </div>

        <div class="scrollable-content">
            <div class="form-container">
                <label>List Title</label>
                <input type="text" id="new-list-title" class="input-field" placeholder="e.g. Gym, Work">
                
                <label>Choose Icon</label>
                <div id="list-category-grid" class="category-grid"></div>

                <label>Date & Time</label>
                <div style="display: flex; gap: 10px;">
                    <input type="date" id="new-list-date" class="input-field">
                    <input type="time" id="new-list-time" class="input-field">
                </div>

                <label>Checklist Items</label>
                <div class="add-item-row">
                    <input type="text" id="new-item-input" class="input-field" placeholder="Add item">
                    <button class="btn-icon-small" onclick="addTempItem()"><span class="material-icons-round">add</span></button>
                </div>
                <div id="temp-items-list" class="temp-tags-container"></div>
                
                <div class="button-row">
                    <button class="btn-primary" onclick="createNewList()">Create</button>
                </div>
            </div>
        </div>
    </div>

</div>

<script>
// --- DATA INIT ---
let users = [];
let activeUserId = null;
let tempUser = { name: "", avatar: "" };
let isCreatingNewUser = false; 
let checklists = [];
let displayedMonth = new Date().getMonth();
let displayedYear = new Date().getFullYear();
let currentDateAPI = new Date();
let tempNewListItems = [];
let currentEditingListId = null;
let isEditMode = false;
let selectedCategory = { icon: 'checklist', color: 'bg-blue' }; 

const avatars = [
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Felix",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Max",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Adrian",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Bella",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Zoe",
    "https://api.dicebear.com/7.x/avataaars/svg?seed=Granny"
];

const categoryOptions = [
    { icon: 'checklist', color: 'bg-blue' },
    { icon: 'directions_run', color: 'bg-purple' },
    { icon: 'pool', color: 'bg-orange' },
    { icon: 'work', color: 'bg-blue' },
    { icon: 'flight', color: 'bg-green' },
    { icon: 'shopping_cart', color: 'bg-gray' },
    { icon: 'hiking', color: 'bg-teal' },
    { icon: 'fitness_center', color: 'bg-red' },
    { icon: 'forest', color: 'bg-green' },
    { icon: 'school', color: 'bg-orange' },
];

document.addEventListener('DOMContentLoaded', () => {
    fetchDateFromAPI();
    setInterval(updateHomeClock, 1000);

    const splash = document.getElementById('splash-screen');
    setTimeout(() => {
        splash.style.opacity = '0';
        setTimeout(() => {
            splash.style.display = 'none';
            if (users.length === 0) {
                startAddUserFlow(); 
            } else {
                navigateTo('home-screen');
            }
        }, 500);
    }, 2000);

    renderCategoryGrid();
    updateProfileDisplay();
    renderApp();
    setupTrashDragDrop();
    setupProfileTrashDragDrop();
});

function formatTime(timeStr) {
    if (!timeStr || timeStr === 'All Day') return 'All Day';
    if(timeStr.includes(':')) {
        const [h, m] = timeStr.split(':');
        if(m === undefined) return timeStr; 
        let hour = parseInt(h);
        const ampm = hour >= 12 ? 'PM' : 'AM';
        hour = hour % 12;
        hour = hour ? hour : 12; 
        return `${hour}:${m} ${ampm}`;
    }
    return timeStr;
}

async function fetchDateFromAPI() {
    try {
        const response = await fetch('http://worldtimeapi.org/api/ip');
        const data = await response.json();
        currentDateAPI = new Date(data.datetime);
        displayedMonth = currentDateAPI.getMonth();
        displayedYear = currentDateAPI.getFullYear();
        renderCalendar();
    } catch (error) {
        currentDateAPI = new Date();
        renderCalendar();
    }
}
function updateHomeClock() {
    const now = new Date(); 
    const hrs = now.getHours();
    const mins = String(now.getMinutes()).padStart(2,'0');
    const ampm = hrs >= 12 ? 'PM' : 'AM';
    const displayHrs = hrs % 12 || 12;
    const el = document.getElementById('current-time-display');
    if(el) el.innerText = `${displayHrs}:${mins} ${ampm}`;
}

function navigateTo(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
    if(screenId === 'home-screen') { renderCalendar(); updateProfileDisplay(); renderApp(); }
    if(screenId === 'profile-screen') updateProfileDisplay();
}

function startAddUserFlow() {
    isCreatingNewUser = true;
    resetUserForm();
    document.getElementById('user-screen-title').innerText = "Add New User";
    
    if(users.length === 0) {
        document.getElementById('user-back-btn').style.display = 'none';
        document.querySelector('#add-user-screen .btn-secondary').style.display = 'none';
    } else {
        document.getElementById('user-back-btn').style.display = 'block';
        document.getElementById('user-back-btn').onclick = () => navigateTo('profile-screen');
        document.querySelector('#add-user-screen .btn-secondary').style.display = 'block';
    }
    navigateTo('add-user-screen');
}

function startEditUserFlow() {
    isCreatingNewUser = false;
    const currentUser = users.find(u => u.id === activeUserId);
    if(!currentUser) return;
    tempUser = { ...currentUser };
    document.getElementById('username-input').value = tempUser.name;
    document.getElementById('setup-main-avatar').src = tempUser.avatar;
    renderAvatarGrid();
    document.getElementById('user-screen-title').innerText = "Edit Profile";
    document.getElementById('user-back-btn').style.display = 'block';
    document.getElementById('user-back-btn').onclick = () => navigateTo('profile-screen');
    document.querySelector('#add-user-screen .btn-secondary').style.display = 'block';
    navigateTo('add-user-screen');
}

function renderAvatarGrid() {
    const grid = document.getElementById('setup-avatar-grid');
    grid.innerHTML = '';
    avatars.forEach(url => {
        const div = document.createElement('div');
        div.className = `avatar-option ${url === tempUser.avatar ? 'selected' : ''}`;
        div.innerHTML = `<img src="${url}">`;
        div.onclick = () => {
            tempUser.avatar = url;
            document.getElementById('setup-main-avatar').src = url;
            renderAvatarGrid();
        };
        grid.appendChild(div);
    });
}
function resetUserForm() {
    tempUser = { name: "", avatar: avatars[0] };
    document.getElementById('username-input').value = "";
    document.getElementById('setup-main-avatar').src = tempUser.avatar;
    renderAvatarGrid();
}
function cancelUserAction() {
    if(users.length > 0) navigateTo('home-screen');
}

function saveUser() {
    const nameVal = document.getElementById('username-input').value.trim();
    if(!nameVal) { alert("Please enter a name"); return; }
    tempUser.name = nameVal;
    
    if (isCreatingNewUser) {
        const newId = Date.now();
        users.push({ id: newId, name: tempUser.name, avatar: tempUser.avatar });
        activeUserId = newId;
    } else {
        const userIndex = users.findIndex(u => u.id === activeUserId);
        if(userIndex > -1) users[userIndex] = { ...users[userIndex], name: tempUser.name, avatar: tempUser.avatar };
    }
    updateProfileDisplay();
    renderApp(); 
    navigateTo('home-screen');
}

function updateProfileDisplay() {
    const currentUser = users.find(u => u.id === activeUserId);
    if(!currentUser) {
        document.getElementById('home-avatar-img').src = '';
        return;
    }
    document.getElementById('home-avatar-img').src = currentUser.avatar;
    document.getElementById('profile-main-avatar').src = currentUser.avatar;
    document.getElementById('profile-display-name').innerText = currentUser.name;

    const otherUsersContainer = document.getElementById('other-users-list');
    otherUsersContainer.innerHTML = '';
    users.forEach(u => {
        const div = document.createElement('div');
        div.className = `small-user-avatar ${u.id === activeUserId ? 'active-user' : ''}`;
        div.innerHTML = `<img src="${u.avatar}">`;
        div.draggable = true;
        div.onclick = () => {
            activeUserId = u.id;
            updateProfileDisplay();
            renderApp(); 
            navigateTo('home-screen');
        };
        div.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/user-id', u.id);
        });
        otherUsersContainer.appendChild(div);
    });
}

function setupProfileTrashDragDrop() {
    const trash = document.getElementById('profile-trash-target');
    trash.addEventListener('dragover', (e) => { e.preventDefault(); trash.classList.add('trash-hover'); });
    trash.addEventListener('dragleave', () => trash.classList.remove('trash-hover'));
    trash.addEventListener('drop', (e) => {
        e.preventDefault(); trash.classList.remove('trash-hover');
        const userId = parseInt(e.dataTransfer.getData('text/user-id'));
        if(userId) deleteUserById(userId);
    });
}

function deleteUserById(id) {
    if(users.length <= 1) { alert("Cannot delete the only user."); return; }
    if(confirm("Delete this user and their data?")) {
        checklists = checklists.filter(item => item.userId !== id);
        users = users.filter(u => u.id !== id);
        if(activeUserId === id) activeUserId = users[0].id;
        updateProfileDisplay();
        renderApp();
    }
}

function changeMonth(dir) {
    displayedMonth += dir;
    if(displayedMonth > 11) { displayedMonth = 0; displayedYear++; }
    if(displayedMonth < 0) { displayedMonth = 11; displayedYear--; }
    renderCalendar();
}

function renderCalendar() {
    const grid = document.getElementById('calendar-days-grid');
    const header = document.getElementById('calendar-month-year');
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    header.innerText = `${monthNames[displayedMonth]} ${displayedYear}`;
    grid.innerHTML = '';
    const firstDayIndex = new Date(displayedYear, displayedMonth, 1).getDay();
    const daysInMonth = new Date(displayedYear, displayedMonth + 1, 0).getDate();
    const userLists = activeUserId ? checklists.filter(c => c.userId === activeUserId) : [];

    for(let i=0; i<firstDayIndex; i++) grid.appendChild(Object.assign(document.createElement('div'), {className: 'day empty'}));

    for(let d=1; d<=daysInMonth; d++) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'day';
        dayDiv.innerText = d;
        const dateString = `${displayedYear}-${String(displayedMonth+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
        if (currentDateAPI.getDate() === d && currentDateAPI.getMonth() === displayedMonth && currentDateAPI.getFullYear() === displayedYear) dayDiv.classList.add('today-marker');
        if(userLists.some(item => item.date === dateString)) dayDiv.classList.add('has-event');
        grid.appendChild(dayDiv);
    }
}

function renderApp() {
    const homeContainer = document.getElementById('home-reminders-list');
    const listsContainer = document.getElementById('all-lists-container');
    homeContainer.innerHTML = ''; listsContainer.innerHTML = '';
    if (!activeUserId) return; 
    const userLists = checklists.filter(c => c.userId === activeUserId);

    userLists.forEach(item => {
        const card = document.createElement('div');
        card.className = 'reminder-card';
        card.onclick = () => openChecklist(item);
        card.innerHTML = `<div class="icon-box ${item.colorClass}"><span class="material-icons-round">${item.icon}</span></div><span class="rem-title">${item.title}</span><span class="rem-date">${formatDate(item.date)}</span><span class="rem-time">${formatTime(item.time)}</span>`;
        homeContainer.appendChild(card);
        
        const li = document.createElement('div');
        li.className = 'list-item';
        li.draggable = true;
        li.addEventListener('dragstart', (e) => { li.classList.add('dragging'); e.dataTransfer.setData('text/list-id', item.id); });
        li.addEventListener('dragend', () => li.classList.remove('dragging'));
        li.onclick = () => openChecklist(item);
        li.innerHTML = `<div class="icon-box ${item.colorClass}"><span class="material-icons-round">${item.icon}</span></div><div class="list-text">${item.title}</div><div style="color: #666; font-size:0.8rem; margin-right:10px;">${formatDate(item.date)} at ${formatTime(item.time)}</div><span class="material-icons-round arrow">chevron_right</span>`;
        listsContainer.appendChild(li);
    });
}

function setupTrashDragDrop() {
    const trash = document.getElementById('trash-target');
    trash.addEventListener('dragover', (e) => { e.preventDefault(); trash.classList.add('trash-hover'); });
    trash.addEventListener('dragleave', () => trash.classList.remove('trash-hover'));
    trash.addEventListener('drop', (e) => {
        e.preventDefault(); trash.classList.remove('trash-hover');
        const id = e.dataTransfer.getData('text/list-id');
        if(id) { checklists = checklists.filter(i => i.id != id); renderApp(); renderCalendar(); }
    });
}

function openChecklist(item) {
    currentEditingListId = item.id;
    isEditMode = false;
    updateChecklistUI(item);
    navigateTo('checklist-screen');
}
function updateChecklistUI(item) {
    document.getElementById('cl-title').innerText = item.title;
    document.getElementById('cl-date').innerText = formatDate(item.date);
    document.getElementById('cl-time').innerText = formatTime(item.time);
    document.getElementById('cl-view-header').style.display = isEditMode ? 'none' : 'block';

    document.getElementById('edit-cl-title').value = item.title;
    document.getElementById('edit-cl-date').value = item.date;
    document.getElementById('edit-cl-time').value = item.time;
    document.getElementById('cl-edit-header').style.display = isEditMode ? 'block' : 'none';

    document.getElementById('cl-edit-icon').innerText = isEditMode ? 'save' : 'edit';
    document.getElementById('cl-action-btn').innerText = isEditMode ? 'Save & Close' : 'Done';
    document.getElementById('cl-action-btn').onclick = isEditMode ? saveChecklistDetails : () => navigateTo('home-screen');

    const container = document.getElementById('cl-items-container');
    container.innerHTML = '';
    item.items.forEach((txt, idx) => {
        if(isEditMode) {
            const row = document.createElement('div');
            row.className = 'checkbox-container';
            row.style.justifyContent = 'space-between';
            row.innerHTML = `<span class="text" style="margin-left:0">${txt}</span><span class="material-icons-round delete-item-icon" onclick="deleteChecklistItem(${idx})">remove_circle</span>`;
            container.appendChild(row);
        } else {
            const label = document.createElement('label');
            label.className = 'checkbox-container';
            label.innerHTML = `<input type="checkbox"><span class="checkmark-box"></span><span class="text">${txt}</span>`;
            container.appendChild(label);
        }
    });
}
function toggleEditChecklistMode() {
    if(isEditMode) saveChecklistDetails();
    else { isEditMode = true; updateChecklistUI(checklists.find(c => c.id == currentEditingListId)); }
}
function saveChecklistDetails() {
    const title = document.getElementById('edit-cl-title').value;
    const date = document.getElementById('edit-cl-date').value;
    const time = document.getElementById('edit-cl-time').value;
    const index = checklists.findIndex(c => c.id == currentEditingListId);
    if(index > -1) { checklists[index].title = title; checklists[index].date = date; checklists[index].time = time; }
    isEditMode = false;
    updateChecklistUI(checklists[index]);
    renderApp(); renderCalendar();
}
function deleteChecklistItem(idx) {
    const index = checklists.findIndex(c => c.id == currentEditingListId);
    if(index > -1) { checklists[index].items.splice(idx, 1); updateChecklistUI(checklists[index]); }
}
function addChecklistItemInEdit() {
    const val = document.getElementById('add-cl-item-input').value.trim();
    if(val) {
        const index = checklists.findIndex(c => c.id == currentEditingListId);
        if(index > -1) { checklists[index].items.push(val); updateChecklistUI(checklists[index]); document.getElementById('add-cl-item-input').value=''; }
    }
}

function renderCategoryGrid() {
    const container = document.getElementById('list-category-grid');
    container.innerHTML = '';
    categoryOptions.forEach(opt => {
        const div = document.createElement('div');
        div.className = `category-option ${opt.color} ${selectedCategory.icon === opt.icon ? 'selected' : ''}`;
        div.innerHTML = `<span class="material-icons-round">${opt.icon}</span>`;
        div.onclick = () => {
            selectedCategory = opt;
            document.querySelectorAll('#list-category-grid .category-option').forEach(el => el.classList.remove('selected'));
            div.classList.add('selected');
        };
        container.appendChild(div);
    });
}

function addTempItem() {
    const val = document.getElementById('new-item-input').value.trim();
    if(val) { tempNewListItems.push(val); renderTempItems(); document.getElementById('new-item-input').value = ''; }
}
function renderTempItems() {
    document.getElementById('temp-items-list').innerHTML = tempNewListItems.map((t, i) => `<div class="temp-tag">${t} <span style="color:red;cursor:pointer;margin-left:5px" onclick="removeTempItem(${i})">×</span></div>`).join('');
}
function removeTempItem(i) { tempNewListItems.splice(i, 1); renderTempItems(); }

function createNewList() {
    const title = document.getElementById('new-list-title').value;
    const date = document.getElementById('new-list-date').value;
    const time = document.getElementById('new-list-time').value;
    if(!title || !date) { alert("Title and Date required"); return; }
    
    checklists.push({ 
        id: Date.now(), 
        userId: activeUserId, 
        title, date, time: time || 'All Day', 
        icon: selectedCategory.icon, 
        colorClass: selectedCategory.color, 
        items: [...tempNewListItems] 
    });
    
    tempNewListItems = []; renderTempItems(); 
    renderApp(); renderCalendar(); 
    navigateTo('lists-screen');
}
function formatDate(isoStr) {
    if(!isoStr) return "";
    const parts = isoStr.split('-');
    return new Date(parts[0], parts[1]-1, parts[2]).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}
</script>
</body>
</html>
"""

# ==========================================
# 3. RENDER THE COMPONENT
# ==========================================
c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    components.html(html_code, height=950, scrolling=True)
