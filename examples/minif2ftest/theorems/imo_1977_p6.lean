--@funsearch.evolve
theorem imo_1977_p6
  (f : ℕ → ℕ)
  (h₀ : ∀ n, 0 < f n)
  (h₁ : ∀ n, 0 < n → f (f n) < f (n + 1)) :
  ∀ n, 0 < n → f n = n := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
