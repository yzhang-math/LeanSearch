--@funsearch.evolve
theorem mathd_numbertheory_427
  (a : ℕ)
  (h₀ : a = (∑ k in (Nat.divisors 500), k)) :
  ∑ k in Finset.filter (λ x => Nat.Prime x) (Nat.divisors a), k = 25 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
