--@funsearch.evolve
theorem amc12a_2013_p7 (s : ℕ → ℝ) (h₀ : ∀ n, s (n + 2) = s (n + 1) + s n) (h₁ : s 9 = 110)
    (h₂ : s 7 = 42) : s 4 = 10 := by
  simp_all only [zero_add]
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
