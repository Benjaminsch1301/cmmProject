Nowcasting Dataloader
========================
by Christopher Ley

How to use
----------
To replicate the environment I used you can install it from the environment.yml file:
~~~console
conda env create -f ./environment.yml
~~~

if you modify the environment you can update the environment.yml file with:
~~~console
conda env export | grep -v "^prefix: " > environment.yml
~~~

### Best practices
It is required that before pushing that the staged commits __pass__ the `pre-commit`, this involves running

    pre-commit run

which will sanitise the currently staged commits according the repositories rules, this may require a few passes and
perhaps manual intervention (fixes). You should be able to run

    pre-commit run --all

without errors, if not please correct before creating a pull request!
These sanitary practices will aid in code readability and speed up pull requests.

Please also strive to write self documenting code or documentation strings were needed (sparingly)!

__Type hints__ are strongly encouraged!
