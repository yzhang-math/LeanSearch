--@funsearch.evolve
theorem aime_1983_p3
  (f : ℝ → ℝ)
  (h₀ : ∀ x, f x = (x^2 + (18 * x +  30) - 2 * Real.sqrt (x^2 + (18 * x + 45))))
  (h₁ : Fintype (f⁻¹' {0})) :
  ∏ x in (f⁻¹' {0}).toFinset, x = 20 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
