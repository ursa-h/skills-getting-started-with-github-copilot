document.addEventListener("DOMContentLoaded", () => {
  async function loadActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();
      const activitiesList = document.getElementById("activities-list");
      const activitySelect = document.getElementById("activity");

      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      Object.entries(activities).forEach(([name, details]) => {
        // Create activity card
        const card = document.createElement("div");
        card.className = "activity-card";

        // Add activity content
        card.innerHTML = `
                <h4>${name}</h4>
                <p>${details.description}</p>
                <p><strong>Schedule:</strong> ${details.schedule}</p>
                <p><strong>Available Spots:</strong> ${details.max_participants - details.participants.length} of ${details.max_participants}</p>
                <div class="participants-list">
                    <h5>Current Participants:</h5>
                    <ul>
                        ${details.participants.map(email => `<li>${email}</li>`).join('')}
                    </ul>
                </div>
            `;

        activitiesList.appendChild(card);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      console.error("Error loading activities:", error);
    }
  }

  loadActivities();

  // Handle form submission
  const form = document.getElementById("signup-form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;
    const messageDiv = document.getElementById("message");

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        }
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Signup failed");
      }

      messageDiv.className = "message success";
      messageDiv.textContent = "Successfully signed up for the activity!";
      messageDiv.classList.remove("hidden");

      // Reload activities to show updated participants
      loadActivities();
      form.reset();
    } catch (error) {
      messageDiv.className = "message error";
      messageDiv.textContent = "Error signing up for the activity. Please try again.";
      messageDiv.classList.remove("hidden");
    }
  });
});
