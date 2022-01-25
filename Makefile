.PHONY: ship


ship:
	rm -rf build/
	rm -rf dist/
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --skip-existing
