resolution_histos_maker.sh

```
python histos_for_resolution.py -i 0 (Se vuoi fare un test su 100.000 entries)
python HoE.py #scrive su file la media delle distribuzioni di H/E in bin di Mee
python res_scale_plotter.py -t HoverE #questo plotta
python res_scale_plotter.py -t HTotoverETot
python res_scale_plotter.py -t HoverE_lowEta
python res_scale_plotter.py -t HoverE_highEta
python res_scale_plotter.py -t HTotoverETot_lowEta
python res_scale_plotter.py -t HTotoverETot_highEta
```