--@funsearch.evolve
theorem mathd_numbertheory_461 (n : ℕ)
  (h₀ : n = Finset.card (Finset.filter (fun x => Nat.gcd x 8 = 1) (Finset.Icc 1 7))) :
  3 ^ n % 8 = 1 := by
  subst h₀
  apply Eq.refl

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
