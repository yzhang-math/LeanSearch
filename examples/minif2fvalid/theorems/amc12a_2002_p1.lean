--@funsearch.evolve
theorem amc12a_2002_p1 (f : ℂ → ℂ) (h₀ : ∀ x, f x = (2 * x + 3) * (x - 4) + (2 * x + 3) * (x - 6))
  (h₁ : Fintype (f ⁻¹' {0})) : (∑ y in (f ⁻¹' {0}).toFinset, y) = 7 / 2 := by
  sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
