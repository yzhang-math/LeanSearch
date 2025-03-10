--@funsearch.evolve
theorem mathd_numbertheory_552
  (f g h : ℕ+ → ℕ)
  (h₀ : ∀ x, f x = 12 * x + 7)
  (h₁ : ∀ x, g x = 5 * x + 2)
  (h₂ : ∀ x, h x = Nat.gcd (f x) (g x))
  (h₃ : Fintype (Set.range h)) :
  ∑ k in (Set.range h).toFinset, k = 12 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
