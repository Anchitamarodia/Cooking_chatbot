import React, { useState } from "react";
import "./App.css";

function App() {
  const [ingredients, setIngredients] = useState("");
  const [dietaryPref, setDietaryPref] = useState("vegetarian");
  const [recipe, setRecipe] = useState("");

  const fetchRecipe = async () => {
    const response = await fetch("http://localhost:5000/get_recipe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients: ingredients.split(","), dietary_pref: dietaryPref }),
    });
    const data = await response.json();
    setRecipe(data.recipe);
  };

  return (
    <div className="App">
      <h1>Indian Cooking Chatbot</h1>
      <input
        type="text"
        placeholder="Enter ingredients (comma-separated)"
        onChange={(e) => setIngredients(e.target.value)}
      />
      <select onChange={(e) => setDietaryPref(e.target.value)}>
        <option value="vegetarian">Vegetarian</option>
        <option value="vegan">Vegan</option>
        <option value="non-vegetarian">Non-Vegetarian</option>
      </select>
      <button onClick={fetchRecipe}>Get Recipe</button>
      <p>{recipe}</p>
    </div>
  );
}

export default App;
