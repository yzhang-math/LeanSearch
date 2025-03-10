--@funsearch.evolve
theorem amc12a_2021_p18
  (f : ℚ → ℝ)
  (h₀ : ∀x>0, ∀y>0, f (x * y) = f x + f y)
  (h₁ : ∀p, Nat.Prime p → f p = p) :
  f (25 / 11) < 0 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
