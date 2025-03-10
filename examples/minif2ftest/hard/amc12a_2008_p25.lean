--@funsearch.evolve
theorem amc12a_2008_p25
  (a b : ℕ → ℝ)
  (h₀ : ∀ n, a (n + 1) = Real.sqrt 3 * a n - b n)
  (h₁ : ∀ n, b (n + 1) = Real.sqrt 3 * b n + a n)
  (h₂ : a 100 = 2)
  (h₃ : b 100 = 4) :
  a 1 + b 1 = 1 / (2^98) := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
