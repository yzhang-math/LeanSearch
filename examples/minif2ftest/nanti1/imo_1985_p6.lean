--@funsearch.evolve
theorem imo_1985_p6
  (f : ℕ → NNReal → ℝ)
  (h₀ : ∀ x, f 1 x = x)
  (h₁ : ∀ x n, f (n + 1) x = f n x * (f n x + 1 / n)) :
  ∃! a, ∀ n, 0 < n → 0 < f n a ∧ f n a < f (n + 1) a ∧ f (n + 1) a < 1 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
