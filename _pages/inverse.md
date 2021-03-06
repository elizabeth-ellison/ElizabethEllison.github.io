---
layout: archive
title: "Glaciological inverse methods"
permalink: /inverse/
author_profile: true
---

<p align="center">
  <img src="https://dngoldberg.github.io/files/inv_cartoon.png?raw=true" alt="Photo" style="width: 350px;"/>
</p>

A common theme in glaciology is the need to measure, or estimate, properties that are not accessible -- because they are hidden under hundreds of meters of ice, or hidden in the past, and there can be other difficulties besides. Consider the relationship between sliding rate and friction force at the bottom of an ice sheet -- the <i>sliding coefficient</i>. It can vary strongly over large expanses -- and it strongly determines how sensitive the ice sheet is to changes in climate -- and its spatial pattern needed as an input to our ice models. We cannot see everywhere under the ice sheet -- and even if we could drill to the bed in a few places, this is not likely to be of value, as there is [no apparent relationship between bed properties and sliding coefficient at a given isolated location](http://onlinelibrary.wiley.com/doi/10.1002/2017JF004373/abstract). Inverse models, however, provide another route. An ice sheet model will use a "guess" for sliding coefficients -- and then, depending on how poorly the result matches observations, it will update its guess until a satisfactory match with observations is found. Much of glaciological inverse modelling deals with effective ways to update this guess. I've had projects involving inverse modelling at a number of different levels over the years, and I continue to try to improve the way we gather information from glaciological data.

---

## Inverse problems with Higher Order glacier mechanics

The example of sliding coefficients above has a long history in the modelling of ice dynamics. [MacAyeal (1992)](http://geosci.uchicago.edu/pdfs/macayeal/Macayeal_ise.pdf) derived a method to greatly speed up the process of improving the "guess" of the sliding coefficient pattern. Termed a _control method_, it solves the _adjoint_ of the linearized ice flow model to find the _search direction_ in which model-observation misfit is optimally minimized. By iteration, an optimal solution is reached. In the quarter-century since, this is still the method of choice for glaciological inversions. Most often it is done using a [Shallow-Shelf Approximation (SSA)](http://www.antarcticglaciers.org/glaciers-and-climate/numerical-ice-sheet-models/hierarchy-ice-sheet-models-introduction/#SECTION_6) flow model.

More recently, _hybrid models_, which retain the ease of solution of the SSA but represent vertical shearing which takes place over a cold bed, which the SSA cannot. The adjoint of a hybrid model was _very carefully_ derived, taking care not to make any approximations (as is usually done for ease of computation). The implications of making such approximations can be seen below in the results of an "identical twin" test, where sliding coefficients are known and model output is treated as data. Using a less accurate adjoint results in a failed recovery of those coefficients.

<p align="center">
  <img src="https://dngoldberg.github.io/files/inverted_profile.png?raw=true" alt="Photo" style="width: 350px;"/>
</p>

#### Relevant publications:
[Goldberg 2011](https://www.cambridge.org/core/journals/journal-of-glaciology/article/variationally-derived-depthintegrated-approximation-to-a-higherorder-glaciological-flow-model/D7F81AD3E98D151FC66E52D272628512) <br />
[Goldberg and Sergienko 2011](https://www.the-cryosphere.net/5/315/2011/)

---

## Automatic Differentiation

An adjoint model is essentially the [derivative](https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant) of a model, and, as discussed above, it is enormously helpful in finding the best set of inputs to provide a desired output. There are two general ways to find the adjoint of a numerical model: (1) Starting from the continuous equations, find the adjoint to these equations and discretise, and (2) Discretise the continuous equations into computer code, and then differentiate the computer code, line by line. Historically (1) has been used for ice model inversions. (2) [has been applied extensively to ocean models](http://www.ecco-group.org/), but its use in ice sheet modelling is limited, which is unfortunate -- applying (1) to a time-dependent ice flow model is not an easy feat! On the other hand, (2) is impractical without the aid of Automatic Differentiation (AD) -- software which applies the "chain rule" of differentiation at the operation level. Examples of AD tools are [TAF](http://www.fastopt.com/products/taf/taf.shtml), [OpenAD](http://www.mcs.anl.gov/OpenAD/), and [Tapenade](https://www-sop.inria.fr/tropics/tapenade.html). Still, if care is not taken in writing the code, the AD tools will not work.

AD tools have been applied to an ice-sheet model developed as part of [MITgcm](https://mitgcm.readthedocs.io/en/latest/phys_pkgs/streamice.html), and more recently with the [FEniCS](https://fenicsproject.org/) software. In a recent study these tools were used to assimilate a decades' worth of remotely observed data and to assess the susceptibility of a fast flowing ice stream to ocean melt, and they are now being used as part of the [International Thwaites Initiative](https://thwaitesglacier.org/projects/prophet)

#### Relevant publications:
[Goldberg and Heimbach 2013](https://www.the-cryosphere.net/7/1659/2013/)<br />
[Goldberg et al 2015](https://www.the-cryosphere.net/9/2429/2015/)<br />
[Goldberg et al 2016](https://www.geosci-model-dev.net/9/1891/2016/)<br />
[Goldberg et al 2018](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2018GL080383)<br />
Maddison, Goldberg and Goddard 2019



