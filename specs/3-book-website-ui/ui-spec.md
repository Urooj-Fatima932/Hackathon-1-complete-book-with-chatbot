# UI Specification: Physical AI & Humanoid Robotics Book Website

## 1. Overview & Design Philosophy

This document specifies the User Interface (UI) and User Experience (UX) for the "Physical AI & Humanoid Robotics" book website.

The design philosophy is **modern, clean, and professional**. The interface will prioritize readability, ease of navigation, and a focused learning environment, drawing inspiration from leading documentation sites like those for Stripe, Vercel, and Figma. The goal is to create a developer-ready specification for a Docusaurus-based website.

## 2. Design System

### 2.1. Color Palette

The palette is designed for clarity and a professional feel, with distinct light and dark modes.

| Mode | Role | Color (HEX) | Notes |
|---|---|---|---|
| Light | Background | `#FFFFFF` | Primary page background |
| Light | Text (Primary) | `#1A202C` | For body copy |
| Light | Text (Secondary) | `#4A5568` | For metadata, subtitles |
| Light | Accent | `#2B6CB0` | For links, buttons, active nav items |
| Light | Accent (Hover) | `#2C5282` | For hover states on accent elements |
| Light | Borders/Dividers | `#E2E8F0` | For cards, separators |
| Dark | Background | `#121212` | Primary page background |
| Dark | Surface | `#1E1E1E` | For cards and sidebars |
| Dark | Text (Primary) | `#E2E8F0` | For body copy |
| Dark | Text (Secondary) | `#A0AEC0` | For metadata, subtitles |
| Dark | Accent | `#63B3ED` | For links, buttons, active nav items |
| Dark | Accent (Hover) | `#90CDF4` | For hover states on accent elements |
| Dark | Borders/Dividers | `#2D3748` | For cards, separators |

### 2.2. Typography

A consistent and readable typography system is crucial. We will use a sans-serif font stack for a modern feel.

- **UI & Headings Font:** `Inter` (or system-ui as a fallback)
- **Body Font:** `Inter` (or system-ui as a fallback)
- **Code Font:** `Fira Code` (or any modern monospace font with ligatures)

| Element | Font Weight | Size (Desktop) | Size (Mobile) | Line Height |
|---|---|---|---|---|
| H1 (Page Title) | Bold (700) | `2.25rem` (36px) | `1.875rem` (30px) | 1.2 |
| H2 | Bold (700) | `1.875rem` (30px) | `1.5rem` (24px) | 1.3 |
| H3 | Semi-Bold (600) | `1.5rem` (24px) | `1.25rem` (20px) | 1.4 |
| Body Text | Regular (400) | `1rem` (16px) | `1rem` (16px) | 1.6 |
| Metadata/Captions | Regular (400) | `0.875rem` (14px) | `0.875rem` (14px) | 1.5 |
| Code Block | Regular (400) | `0.9rem` (14.4px) | `0.9rem` (14.4px) | 1.5 |

### 2.3. Spacing & Layout

- **Base Unit:** `8px`. All padding, margins, and layout spacing will be multiples of this unit (e.g., 8px, 16px, 24px, 32px).
- **Max Content Width:** `80ch` for the main content area to ensure optimal readability.
- **Grid:** A standard 12-column grid will be used for complex layouts (like the homepage).

### 2.4. Components

- **Buttons (CTA):**
  - **Primary:** Solid `Accent` color background, white text. `16px` padding on sides, `12px` on top/bottom. `8px` border radius. Subtle box-shadow on hover.
  - **Secondary:** `Accent` color border, `Accent` color text, transparent background. Same padding and radius. Fills with `Accent` color on hover.
- **Cards:** Used for module overviews on the homepage.
  - `Surface` color background, `Borders/Dividers` color for border.
  - `16px` border radius.
  - `24px` padding.
  - Subtle box-shadow that increases on hover to provide a "lift" effect.

## 3. Page Specifications

### 3.1. Home Page

- **Layout:**
  - **Hero Section:** Centered text alignment. Title (H1), a 2-3 sentence subtitle, and a primary CTA button ("Start Learning").
  - **Features/Modules Overview:** A 2x2 grid of Cards, one for each of the 4 modules. Each card contains a module icon (placeholder), module title (H3), and a brief description.
  - **Footer:** A full-width bar with three columns: (1) Contact/About, (2) GitHub Repo Link, (3) Hackathon Info.
- **Placeholders:**
  - `[Illustration: Abstract representation of Humanoid Robotics | 1200x500]` in the hero section background.
  - `[Icon: Module 1-4 | 48x48]` for each module card.

### 3.2. Content Page (Module & Chapter)

This is the primary view for reading the book.

- **Layout:** Three-column layout.
  - **Left Sidebar (Main Navigation):**
    - `280px` wide on desktop.
    - Collapsible on tablet/mobile (hamburger menu in top bar).
    - Tree structure: Module (non-collapsible) -> Week (collapsible) -> Chapter.
    - The currently active chapter link is highlighted with `Accent` color.
  - **Center Column (Main Content):**
    - Takes the remaining width, with a max-width for readability.
    - Displays the `.mdx` content.
    - Contains all sections from the Chapter Template.
  - **Right Sidebar (On-This-Page):**
    - `240px` wide on desktop.
    - Hidden on tablet/mobile.
    - Automatically generated table of contents from the current page's H2 and H3 headings.
- **Components:**
  - **Code Blocks:** Displayed in a `Surface` colored container, with syntax highlighting and a "Copy" button in the top-right corner.
  - **Image Placeholders:** A dashed border box with the color `Borders/Dividers`. Inside, centered text indicates the required content and dimensions (e.g., `[Diagram: ROS 2 Node Graph | 800x400]`).
  - **Next/Previous Buttons:** Placed at the bottom of the main content area. Styled as secondary buttons.

## 4. Global Navigation

- **Top Bar / Header:**
  - `64px` height, with a `Borders/Dividers` bottom border.
  - **Left:** Book Title. On mobile, a hamburger icon to toggle the main navigation sidebar.
  - **Right:** Global Search bar, Light/Dark mode toggle icon, and a link to the GitHub repository.
- **Search:**
  - A click on the search bar opens a centered modal for the search interface (Algolia DocSearch style).
  - Results are displayed instantly in the modal.

## 5. Functional & UX Requirements

| ID | Requirement | Acceptance Criteria |
|---|---|---|
| UI-1 | **Responsiveness** | All pages and layouts MUST adapt gracefully to screen sizes from 320px (mobile) to 1920px+ (large desktop). The three-column layout must collapse to a single column on mobile. |
| UI-2 | **Dark Mode** | Users MUST be able to toggle between light and dark modes. The choice MUST be persisted across sessions (using localStorage). |
| UI-3 | **Interactive Code Blocks** | All code blocks MUST feature syntax highlighting and a one-click "Copy to Clipboard" button. A success indicator (e.g., checkmark) should appear briefly after clicking. |
| UI-4 | **Collapsible Navigation** | The main navigation sidebar MUST be collapsible on mobile/tablet views and accessible via a hamburger menu icon in the top bar. |
| UI-5 | **Accessible Design** | All components must meet WCAG 2.1 AA standards for color contrast and keyboard navigation. |
| UI-6 | **Hover & Active States** | All interactive elements (links, buttons, navigation items) MUST have distinct hover and active/focus states to provide clear visual feedback. |
