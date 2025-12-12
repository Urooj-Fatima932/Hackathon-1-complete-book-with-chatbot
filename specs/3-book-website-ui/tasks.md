# Tasks: Physical AI & Humanoid Robotics Book Website UI

**Input**: Design documents from `/specs/3-book-website-ui/`
**Prerequisites**: plan.md (required), ui-spec.md (required), research.md (if available)

## Phase 1: Global Design Setup

- [X] T001 Define color palette in CSS with light/dark mode variables as specified in UI spec
- [X] T002 Set up typography system with Inter and Fira Code fonts as specified
- [X] T003 Implement spacing system using 8px base unit as specified in design system
- [X] T004 Create button components (primary/secondary) with hover effects as specified
- [X] T005 Create card components with specified styling (16px radius, 24px padding)
- [X] T006 Set up responsive breakpoints for desktop, tablet, and mobile

## Phase 2: Home Page Implementation

- [X] T007 Create hero section with centered title, subtitle, and "Start Learning" CTA
- [X] T008 Implement features/modules overview as 2x2 grid of card components
- [X] T009 Add placeholder illustrations and icons for each module card
- [X] T010 Create footer with three-column layout (Contact/About, GitHub, Hackathon)
- [X] T011 Add hover effects to cards with lift effect as specified
- [X] T012 Make homepage responsive for all device sizes

## Phase 3: Navigation System

- [X] T013 Implement main navigation sidebar (280px wide) with collapsible mobile menu
- [X] T014 Create top bar header with book title, search, and GitHub link
- [X] T015 Implement "On This Page" right sidebar for chapter navigation (240px wide)
- [X] T016 Create navigation tree: Module → Week → Chapter as specified
- [X] T017 Add active chapter highlighting with accent color

## Phase 4: Module Pages Implementation

- [X] T018 Create module header with title information
- [X] T019 Display week and chapter list in main navigation sidebar
- [X] T020 Show chapter previews with brief descriptions
- [X] T021 Add "Go to Chapter" CTA buttons for each preview
- [X] T022 Add placeholder images/diagrams for module content
- [X] T023 Ensure responsive design for module pages

## Phase 5: Chapter Pages Implementation

- [X] T024 Create chapter header with title and module/week info
- [X] T025 Implement three-column layout (sidebar, content, TOC) as specified
- [X] T026 Add code blocks with syntax highlighting and copy button
- [X] T027 Implement placeholder styling with dashed borders and dimension labels
- [X] T028 Add next/previous chapter navigation buttons
- [X] T029 Ensure responsive design (collapses to single column on mobile)
- [X] T030 Add WCAG 2.1 AA compliant accessibility features

## Phase 6: Testing & Validation

- [X] T031 Verify color contrasts meet WCAG 2.1 AA standards
- [X] T032 Validate responsive design on mobile, tablet, desktop
- [X] T033 Test interactive code blocks with copy functionality
- [X] T034 Verify collapsible navigation works on mobile/tablet
- [X] T035 Test light/dark mode toggle persistence across sessions
- [X] T036 Validate all placeholder elements render correctly
