const API_BASE = "https://herforecast.onrender.com";

/**
 * Fetch predicted phase for a given user (optional day).
 */
export async function fetchPrediction(userId, day) {
  const params = new URLSearchParams({ id: String(userId) });
  if (day !== undefined) params.set("day", String(day));

  const res = await fetch(`${API_BASE}/predict?${params}`);

  if (!res.ok) {
    throw new Error(`Prediction request failed: ${res.status}`);
  }

  return res.json();
}

/**
 * Fetch available users.
 */
export async function fetchUsers() {
  const res = await fetch(`${API_BASE}/users`);

  if (!res.ok) {
    throw new Error(`Users request failed: ${res.status}`);
  }

  const data = await res.json();
  return data.users;
}

/**
 * Fetch timeline for a user.
 */
export async function fetchTimeline(userId) {
  const res = await fetch(`${API_BASE}/user/${userId}/timeline`);

  if (!res.ok) {
    throw new Error(`Timeline request failed: ${res.status}`);
  }

  return res.json();
}

/**
 * Fetch model info.
 */
export async function fetchModelInfo() {
  const res = await fetch(`${API_BASE}/model/info`);

  if (!res.ok) {
    throw new Error(`Model info request failed: ${res.status}`);
  }

  return res.json();
}

/**
 * Simulate prediction using wearable + hormone data.
 */
export async function simulatePrediction(data) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error(`Simulation request failed: ${res.status}`);
  }

  return res.json();
}
