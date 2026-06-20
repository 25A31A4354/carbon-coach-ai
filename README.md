# CarbonCoach AI 🌱

> **"Your Personal Carbon Reduction Assistant"**

A smart sustainability assistant that helps users understand, track, and reduce their carbon footprint through personalized coaching, impact simulations, and actionable missions.

---

## 🎯 Problem Statement

Many people want to live sustainably but struggle because they don't know:
- Which of their habits contribute most to their carbon footprint
- Which specific actions will have the biggest impact
- Where to start

Most carbon footprint tools only provide abstract numbers and statistics, but fail to guide users toward meaningful and sustained action.

---

## 💡 Solution Overview

**CarbonCoach AI** goes beyond traditional carbon calculation. It analyzes a user's lifestyle habits and acts as a personal sustainability coach. 

The platform actively:
- Identifies the user's biggest carbon leak
- Generates personalized, highly-actionable reduction missions
- Simulates future environmental impact to visualize change
- Estimates potential financial savings tied to sustainable habits
- Provides contextual coaching and clear reasoning behind every recommendation

---

## ✨ Key Features

### 🔍 Carbon Leak Detection
Identifies the highest-impact source of avoidable emissions in a user's daily life.

### 🎯 Personalized Carbon Missions
Generates realistic, achievable weekly actions tailored specifically to the user's current habits.

### 🔮 Future Impact Simulator
Visualizes a comparison between the user's current footprint and their improved future footprint.

### 👤 Carbon Persona Engine
Creates a unique sustainability profile and archetype based on the user's specific answers.

### 💰 Savings Impact Engine
Shows estimated financial savings (in INR) alongside carbon reduction to connect sustainability with personal financial benefit.

### 📈 Progress Tracking
A lightweight gamification system that tracks continuous mission completion and daily streaks.

### 🧠 Assistant Reasoning Layer
Transparently explains exactly why specific recommendations were selected and why they are the highest impact option for the user.

---

## ⚙️ How It Works

1. **User completes lifestyle assessment**: The user answers questions regarding their Transport, Food, Energy, and Shopping habits.
2. **CarbonCoach AI analyzes patterns**: The backend dynamically evaluates the environmental impact of these choices.
3. **The system identifies**: The algorithm isolates the largest carbon leak and the highest-impact improvement opportunity.
4. **A personalized mission is generated**: A targeted, realistic weekly mission is created to plug the carbon leak.
5. **Future impact and savings are displayed**: The user is presented with their potential carbon reduction, financial savings, and global impact motivation.
6. **User tracks progress over time**: Users can accept missions and build sustainable streaks.

---

## 🧠 Smart Decision-Making Logic

The platform does not simply calculate emissions. It intelligently prioritizes actions based on a balance of:
- **Potential carbon reduction**
- **User effort required**
- **Practical feasibility**

This logic ensures users receive recommendations that are both highly impactful and actually achievable in their day-to-day lives.

---

## 🛠 Technology Stack

**Frontend:**
- HTML
- CSS
- JavaScript

**Backend:**
- Python
- Flask

**AI Integration:**
- Gemini API *(for personalized coaching, contextual explanations, and persona generation)*

**Storage:**
- Local storage / application state *(no accounts required)*

**Testing:**
- Unit tests (Pytest)

---

## 🏗 Architecture Overview

```text
Input Layer
   ↓
Behavior Analysis Engine
   ↓
Carbon Leak Detection
   ↓
Mission Generation
   ↓
Future Impact Simulator
   ↓
Assistant Coaching Layer
   ↓
User Dashboard
```

---

## 🏆 Alignment with Challenge Objectives

### Smart Dynamic Assistant
Provides highly contextual coaching and personalized recommendations tailored to individual users.

### Logical Decision Making
Uses intelligent logic over user habits to dynamically determine the absolute highest-impact actions.

### Practical Usability
Focuses entirely on real-world actions, financial savings, and simple behavioral changes instead of only showing carbon scores.

### Real Impact
Encourages and tracks measurable behavior change through streaks and realistic missions.

---

## ♿ Accessibility

- **Semantic HTML**: Ensures screen readers can navigate effectively.
- **Accessible Forms**: Properly labeled inputs and states.
- **Keyboard Navigation**: Fully operable without a mouse.
- **High Contrast UI**: Thoughtful color palettes for maximum readability.
- **Responsive Design**: Flawless experience on mobile, tablet, and desktop devices.

---

## 🔒 Security

- **Input Validation**: Server-side checks for all payload data.
- **Sanitized User Inputs**: Prevents malicious data injection.
- **Safe API Handling**: Robust try-catch logic with safe environmental fallbacks.
- **Error Handling**: Graceful degradation when external services are unavailable.

---

## 🧪 Testing

- **Unit Tests**: Coverage for the core analysis engine and fallback logic.
- **Validation Tests**: Ensures invalid payloads are rejected safely.
- **Logic Verification Tests**: Confirms the highest-impact leak is accurately identified.

---

## 🚀 Future Scope

- **Real Carbon Datasets**: Integration with live, localized grid emission APIs.
- **Mobile App Version**: A dedicated native mobile application for better push notifications.
- **Community Challenges**: Localized sustainability challenges with friends.
- **Team Sustainability Goals**: Enterprise mode for corporate ESG tracking.
- **Carbon Reduction Leaderboards**: Gamified global rankings for carbon reduction.

---

## 🌎 Conclusion

**CarbonCoach AI** transforms carbon awareness into meaningful action by helping users discover the single most effective change they can make, and gently guiding them through a realistic, personalized sustainability journey.
