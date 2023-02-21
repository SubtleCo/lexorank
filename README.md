# Lexorank
"Lexicographical ranking", originally coined by Jira in their "LexoRank" algorithm, is a user driven sorting algorithm that utilizes the optimization of alphabetical string sorting over numerical sorting to make quick, atomic calculations to reorder a list when a user changes the order of a list, perhaps through a "drag & drop" motion.

Let's see it in action first, and then describe what's going on under the hood.

## To run:

For clean output:
`python rank.py x y`
where `x=` your low rank as a lowercase string i.e. `abc`
and `y=` your low rank as a lowercase string i.e. `def`

For debugged output:
`python rank.py x y debug`


## How it works
Lexicographical ranking uses a Base26 cipher (a=0 ... z=25) to order a list of items. When a rank is calculated, a numerical mean between the surrounding items is converted to a "lexorank". Once the data is refetched from the source, ordered by rank, ascending, the list of items will be in the user defined order. By using the mean, we're able to provide a good deal of "padding" between ranks for future operations. For instance, if we have four items ranked `aaaaaa=0, iririr=102971925, ririri=205943850, zzzzzz=308915775`, that means we've got about 102 million spots between each item. Room to grow and then some.

### Why not use numbers?
Numbers are nice, but when conflicts arise (i.e. two items want to share the rank `123`), we'd have to rebalance the whole table to regain padding between ranks again. That's a costly operation that we want to avoid as much as we can.

Strings are a lot more forgiving. As humans, we have the luxury of not even having to know the whole string before sorting it.
For instance, if I asked you to sort `bksjdfnr` and `csdlfkjgbl` alphabetically, you'd likely do the natural think and just check the first letter. `b` goes before `c`. Nice. Done. Now, if I asked you to sort `7665165318876` and `14645452163301`, that's gonna take a few extra mental steps.

#### But computers can sort numbers faster than strings!
True, but let's get back to that conflict where we want to place one item after another, but the newly calculated rank AND the rank of the item above are both `123`. The next item is rank `124`. (yes, we could use floats, but that's just delaying the inevitable). 

| Item         | Price     | # In stock |
|--------------|-----------|------------|
| Spicy | 1.99      | *7*        |
| Sweet      | **1.89**  | 5234       |
| Savory      | **1.89**  | 5234       |
