# Setup:

** - Create some postgres cluster
** - Include cluster connection info in node_config.py
** - Run main.py to test the project

* Project structure:
- commands.py: sql command templates.
- init.py: connect to clusters, create metadata tables on coordinator
- node_config.py: clusters connection info
- querry_planner: distribute querry to workers nodes
- utils.py: utility functions


