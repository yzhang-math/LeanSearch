--@funsearch.evolve
theorem mathd_numbertheory_483
  (a : ℕ → ℕ)
  (h₀ : a 1 = 1)
  (h₁ : a 2 = 1)
  (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) :
  (a 100) % 4 = 3 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
