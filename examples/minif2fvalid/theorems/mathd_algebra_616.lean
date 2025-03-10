--@funsearch.evolve
theorem mathd_algebra_616 (f g : ℝ → ℝ) (h₀ : ∀ x, f x = x ^ 3 + 2 * x + 1)
    (h₁ : ∀ x, g x = x - 1) : f (g 1) = 1 := by
  simp_all

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
