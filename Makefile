.PHONY: notebook app docs

notebook:
	uv run jupyter-notebook .

app:
	uv run streamlit run src/meterviewer/fastview/home.py --browser.gatherUsageStats false

docs:
	uv run sphinx-autobuild -c ./docs/ -b html docs/source docs/build --port 49527