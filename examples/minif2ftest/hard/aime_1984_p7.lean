--@funsearch.evolve
theorem aime_1984_p7
  (f : ℤ → ℤ)
  (h₀ : ∀ n, 1000 ≤ n → f n = n - 3)
  (h₁ : ∀ n, n < 1000 → f n = f (f (n + 5))) :
  f 84 = 997 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
