Welcome to aiomcstats's documentation!
======================================

Aiomcstats is an asyncronous python wrapper for the Hypixel api with 100% coverage.

Requirements
------------

- Python 3.8+
- Pydantic
- Aiohttp

Installation
------------

To install Aiomcstats,
run this command in your terminal or use your favourite package manager:

.. code-block:: console

   $ pip install aiomcstats

Basic Example
-------------

.. code-block:: python

   import aiomcstats
   import asyncio

   async def main():
      data = aiomcstats.status("hypixel.net")
      print(data)


   asyncio.run(main())

.. _Contributor Guide: contributing.html

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   index
   reference
   contributing
   codeofconduct
   license
