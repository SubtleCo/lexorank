# Lexorank
"Lexicographical ranking", originally coined by Jira in their "LexoRank" algorithm, is a user driven sorting algorithm that utilizes the optimization of alphabetical string sorting over numerical sorting to make quick, atomic calculations to reorder a list when a user changes the order of a list, perhaps through a "drag & drop" motion.

Let's see it in action first, and then describe what's going on under the hood.

## To run:

For clean output:\
`python rank.py x y`
where `x=` your low rank as a lowercase string i.e. `bcd`
and `y=` your low rank as a lowercase string i.e. `deg`

```
❯ python rank.py bcd deg
====================
Low rank was      "bcd"
High rank was     "deg"
The new rank is   "cde"

The sorted order, ASC, should be ['bcd', 'cde', 'deg']

The actual sorted order is       ['bcd', 'cde', 'deg']

====================
```

For debugged output:
`python rank.py x y debug`

```
❯ python rank.py bcd deg debug
====================
Low rank was      "bcd"
High rank was     "deg"
The new rank is   "cde"

The sorted order, ASC, should be ['bcd', 'cde', 'deg']

The actual sorted order is       ['bcd', 'cde', 'deg']

====================
debug='debug'
low_rank='bcd'
high_rank='deg'
cipher_length=3
[1, 2, 3]
[3, 4, 6]
padded_low=[1, 2, 3]
padded_high=[3, 4, 6]
numerical_low=731
numerical_high=2138
mean=1434
rebased_number=[2, 3, 4]
new_rank='cde'
valid_rank='cde'
```
## What this project does
- Generate a bulk list of lexoranks for a given number of items. Useful for:
 - Introducing lexorank to an existing project
 - Rebalancing the table, if necessary
- Calculate a new rank given the "previous" and "next" rank

## How it works
Lexicographical ranking uses a Base26 cipher (a=0 ... z=25) to order a list of items. When a rank is calculated, a numerical mean between the surrounding items is converted to a "lexorank". Once the data is refetched from the source, ordered by rank, ascending, the list of items will be in the user defined order. By using the mean, we're able to provide a good deal of "padding" between ranks for future operations. For instance, if we have four items ranked `aaaaaa=0, iririr=102971925, ririri=205943850, zzzzzz=308915775`, that means we've got about 102 million spots between each item. Room to grow and then some.

### Why not use numbers?
Numbers are nice, but when conflicts arise (i.e. two items want to share the rank `123`), we'd have to rebalance the whole table to regain padding between ranks again. That's a costly operation that we want to avoid as much as we can.

Strings are a lot more forgiving. As humans, we have the luxury of not even having to know the whole string before sorting it.
For instance, if I asked you to sort `bksjdfnr` and `csdlfkjgbl` alphabetically, you'd likely do the natural think and just check the first letter. `b` goes before `c`. Nice. Done. Now, if I asked you to sort `7665165318876` and `14645452163301`, that's gonna take a few extra mental steps.

#### But computers can sort numbers faster than strings!
True, but let's get back to that conflict where we want to place one item after another, but the newly calculated rank AND the rank of the item above are both `123`. The next item is rank `124`. (yes, we could use floats, but that's just delaying the inevitable). 

In this example, I want to move `Savory` between `Spicy` and `Sweet`, but given that there's no integer between `123` and `124`, I'd need to rebalance the whole table.

| Item         | Rank  |
|--------------|-------|
| Spicy        | 123   |
| Sweet        | 124   |
| Savory       | 125   |

Now let's look at that same example with lexoranks.

| Item         | Rank  |
|--------------|-------|
| Spicy        | abc   |
| Sweet        | abd   |
| Savory       | abe   |

To move `savory` up, I need a rank between `abc` and `abd`. Ah, here's the beauty of string ranking:
  **If I throw literally any letter at the end of `abc` it will fit between `abc` and `abd`**
Rather than choosing a random letter, let's choose the one smack dab in the middle of the alphabet: **n**\
We've just opened up 12 or 13 ranks on either side! This is a method I've come to call **n-tacking** (tacking an 'n' on the end!)

Let's see it in action:

| Item         | Rank  |
|--------------|-------|
| Spicy        | abc   |
| Savory       | abcn  |
| Sweet        | abd   |

Really great news. We were able to solve the conflict with my very good friend `n`. Thank you, `n`. We didn't have to rebalance anything, which brings up the point of lexicographical ranking:

**When sorting, you only need to operate on a single item / document / database row**

#### Rebalancing
Now then, nothing is truly infinite in computing. Let's say you created the rank column in your database to hold a string of length 255. If you were to use this algorithm indefinitely with no cleanup action, you may eventually run out of room, and rebalancing is necessary. No problem. Just called the original `create_bulk_rank` function. That might chew up a bit of computing resources, but we should only have to do this extremely sparingly, and, hey, the computer's doing it, not you.

