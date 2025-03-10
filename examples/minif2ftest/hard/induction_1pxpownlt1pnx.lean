--@funsearch.evolve
theorem induction_1pxpownlt1pnx
  (x : ℝ)
  (n : ℕ)
  (h₀ : -1 < x)
  (h₁ : 0 < n) :
  (1 + ↑n*x) ≤ (1 + x)^(n:ℕ) := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
