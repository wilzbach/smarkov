smarkov
=======

Simple, lightweight and easy to read implementation of Markov chains and HMMs.

This is a toy project, don't expect any exciting speeds or robustness.

Happy hacking!


Installing
----------

```
pip3 install git+git://github.com/greenify/smarkov.git
```

Hacking
-------

```
git clone https://github.com/greenify/smarkov
cd smarkov
python3 setup.py develop
```

Train with a corpus
-------------------

```
from smarkov import Markov
chain = Markov(["AGACAGACGAC"])
```

### Attributes

corpus: given corpus (a corpus_entry needs to be a tuple or array)  
order: maximal order to look back for a given state (default 1)
tokenize: function how to split an element of the corpus (e.g sentences into words)

Generate text from a chain
--------------------------

```
print("".join(chain.generate_text()))
```

`Generate_text()` generates exactly one element from the Markov chain.
In other words: It goes in the Markov chain the universal start state
to universal end state.

More Examples
--------

See `examples`

Coming
------

Documentation how to use it with HMM.

License
-------

MIT
