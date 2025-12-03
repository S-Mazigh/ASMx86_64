.. ASMx86_64 documentation master file, created by
   sphinx-quickstart on Wed Oct 30 13:17:31 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ASMx86_64
=========

.. container:: text-center

   .. image:: _static/athlon.png
      :alt: ASM x86_64 Logo
      :width: 220px

   .. raw:: html
   
      <h2 style="font-size: 2.5rem; margin: 1rem 0;">
         <strong>ASMx86_64</strong>
      </h2>

   .. raw:: html

      <p style="font-size: 1.1rem;">
         Ce document propose une introduction à la programmation en assembleur x86_64 en utilisant la syntaxe AT&T.
      </p>


.. Navigation pour la barre latérale
.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Notions préalables
   
   Rappels-Système
   Rappels-Compilation

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Syntaxe et bases
   
   x86_64-LesSyntaxes
   x86_64-LesBases
   x86_64-LesFonctions
   x86_64-Alignement

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Travaux pratiques
   
   Instructions-x86_64
   Atou-Analysis
   Tape3

.. Affichage visuel avec grilles
.. grid:: 1 1 2 3
   :gutter: 3

   .. grid-item-card:: :octicon:`sync` Notions préalables
      
      * :doc:`Rappels-Système`
      * :doc:`Rappels-Compilation`

   .. grid-item-card:: :octicon:`book` Syntaxe et bases
      
      * :doc:`x86_64-LesSyntaxes`
      * :doc:`x86_64-LesBases`
      * :doc:`x86_64-LesFonctions`
      * :doc:`x86_64-Alignement`

   .. grid-item-card:: :octicon:`code-square` Travaux pratiques
      
      * :doc:`Instructions-x86_64`
      * :doc:`Atou-Analysis`
      * :doc:`Tape3`

..    :maxdepth: 1
..    :caption: Annexes

..    glossaire

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
