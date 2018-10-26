"""
Plot resonator data and fits on matplotlib Axes.
"""
from __future__ import absolute_import, division, print_function

import matplotlib.pyplot as plt

try:
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']  # matplotlib >= 1.5
except KeyError:
    color_cycle = plt.rcParams['axes.color_cycle']  # matplotlib < 1.5
import numpy as np

default_num_model_points = 10000

measurement_defaults = {'linestyle': 'none',
                        'marker': '.',
                        'markersize': 2,
                        'color': 'gray',
                        'alpha': 1,
                        'label': 'data'}

best_fit_defaults = {'linestyle': '-',
                     'linewidth': 0.3,
                     'color': color_cycle[0],
                     'alpha': 1,
                     'label': 'best fit'}

initial_fit_defaults = {'linestyle': '--',
                        'linewidth': 0.3,
                        'color': color_cycle[1],
                        'alpha': 1,
                        'label': 'initial fit'}

resonance_defaults = {'linestyle': 'none',
                      'marker': '.',
                      'markersize': 3,
                      'alpha': 1,
                      'label': 'resonance'}

photon_number_defaults = {'linestyle': '-',
                          'linewidth': 0.3,
                          'color': color_cycle[0],
                          'alpha': 1}

triptych_figure_defaults = {}

triptych_gridspec_defaults = {'hspace': 0.4,
                              'wspace': 0.4}

frequency_scale_to_unit = {1: 'Hz',
                           1e-3: 'kHz',
                           1e-6: 'MHz',
                           1e-9: 'GHz',
                           1e-12: 'THz'}


def magnitude_vs_frequency(resonator, axes=None, normalize=False, num_model_points=default_num_model_points,
                           frequency_scale=1, three_ticks=True, decibels=True, label_axes=True,
                           plot_measurement=True, plot_best_fit=True, plot_initial_fit=False, plot_resonance=True,
                           measurement_settings=None, best_fit_settings=None, initial_fit_settings=None,
                           resonance_settings=None, **subplots_kwds):
    """
    On the given axis, plot magnitude versus frequency of any or all of the following: the measurement data, the
    best-fit model, and the initial-fit model.

    :param resonator: an instance of a fitter.ResonatorFitter subclass.
    :param axes: a matplotlib Axes instance; if None, create new Figure and Axes objects using
      `fig, ax = plt.subplots(**subplots_kwds)`, plot using these, and return them.
    :param normalize: if True, normalize all of the plotted values to the resonator plane by dividing them by the
      best-fit background model values.
    :param num_model_points: the number of points at which to evaluate the model over the measurement frequency range.
    :param frequency_scale: a float by which the plotted frequencies are multiplied; if this is an integer power of
      10^-3, then automatic horizontal axis label will have the correct units of Hz, kHz, etc.
    :param three_ticks: if True, the horizontal axis will have exactly three tick marks at the minimum frequency,
      resonance frequency, and maximum frequency.
    :param decibels: if True, plot the magnitude in dB instead of dimensionless scattering parameter units, i.e. V / V.
    :param label_axes: if True, give the axes reasonable labels; see also `frequency_scale`.
    :param plot_measurement: if True, plot the measured data.
    :param plot_best_fit: if True, plot the best-fit model.
    :param plot_initial_fit: if True, plot the initial-fit model.
    :param plot_resonance: if True, plot the best-fit and/or initial-fit model data at the corresponding resonance
      frequency.
    :param measurement_settings: a dict of pyplot.plot keywords used to plot the measurement values; see
      `measurement_defaults` in this module.
    :param best_fit_settings: a dict of pyplot.plot keywords used to plot the best-fit model values; see
    `best_fit_defaults` in this module.
    :param initial_fit_settings: a dict of pyplot.plot keywords used to plot the initial-fit modle values; see
      `initial_fit_defaults` in this module.
    :param resonance_settings: a dict of pyplot.plot keywords used to plot the best-fit and/or initial-fit values at the
      corresponding resonance frequency(ies); see `resonance_defaults` in this module.
    :return: if axes is None, return a new Figure and Axes objects; otherwise, return None.
    """
    if decibels:
        scaler = lambda data: 20 * np.log10(np.abs(data))
        vertical_label = 'magnitude / dB'
    else:
        scaler = lambda data: np.abs(data)
        vertical_label = 'magnitude'
    return _plot_vs_frequency(resonator, scaler, vertical_label, axes, normalize, num_model_points, frequency_scale,
                              three_ticks, label_axes, plot_measurement, plot_best_fit, plot_initial_fit,
                              plot_resonance, measurement_settings, best_fit_settings, initial_fit_settings,
                              resonance_settings, **subplots_kwds)


def phase_vs_frequency(resonator, axes=None, normalize=False, num_model_points=default_num_model_points,
                       frequency_scale=1, three_ticks=True, degrees=True, label_axes=True,
                       plot_measurement=True, plot_best_fit=True, plot_initial_fit=False, plot_resonance=True,
                       measurement_settings=None, best_fit_settings=None, initial_fit_settings=None,
                       resonance_settings=None, **subplots_kwds):
    """
    On the given axis, plot phase versus frequency of any or all of the following: the measurement data, the
    best-fit model, and the initial-fit model.

    :param resonator: an instance of a fitter.ResonatorFitter subclass.
    :param axes: a matplotlib Axes instance; if None, create new Figure and Axes objects using
      `fig, ax = plt.subplots(**subplots_kwds)`, plot using these, and return them.
    :param normalize: if True, normalize all of the plotted values to the resonator plane by dividing them by the
      best-fit background model values.
    :param num_model_points: the number of points at which to evaluate the model over the measurement frequency range.
    :param frequency_scale: a float by which the plotted frequencies are multiplied; if this is an integer power of
      10^-3, then automatic horizontal axis label will have the correct units of Hz, kHz, etc.
    :param three_ticks: if True, the horizontal axis will have exactly three tick marks at the minimum frequency,
      resonance frequency, and maximum frequency.
    :param degrees: if True, plot the phase in degrees instead of radians.
    :param label_axes: if True, give the axes reasonable labels; see also `frequency_scale`.
    :param plot_measurement: if True, plot the measured data.
    :param plot_best_fit: if True, plot the best-fit model.
    :param plot_initial_fit: if True, plot the initial-fit model.
    :param plot_resonance: if True, plot the best-fit and/or initial-fit model data at the corresponding resonance
      frequency.
    :param measurement_settings: a dict of pyplot.plot keywords used to plot the measurement values; see
      `measurement_defaults` in this module.
    :param best_fit_settings: a dict of pyplot.plot keywords used to plot the best-fit model values; see
    `best_fit_defaults` in this module.
    :param initial_fit_settings: a dict of pyplot.plot keywords used to plot the initial-fit modle values; see
      `initial_fit_defaults` in this module.
    :param resonance_settings: a dict of pyplot.plot keywords used to plot the best-fit and/or initial-fit values at the
      corresponding resonance frequency(ies); see `resonance_defaults` in this module.
    :return: if axes is None, return a new Figure and Axes objects; otherwise, return None.
    """
    if degrees:
        scaler = lambda data: np.degrees(np.angle(data))
        vertical_label = 'phase / deg'
    else:
        scaler = lambda data: np.angle(data)
        vertical_label = 'phase / rad'
    return _plot_vs_frequency(resonator, scaler, vertical_label, axes, normalize, num_model_points, frequency_scale,
                              three_ticks, label_axes, plot_measurement, plot_best_fit, plot_initial_fit,
                              plot_resonance, measurement_settings, best_fit_settings, initial_fit_settings,
                              resonance_settings, **subplots_kwds)


def _plot_vs_frequency(resonator, scaler, vertical_label, axes=None, normalize=False,
                       num_model_points=default_num_model_points, frequency_scale=1, three_ticks=True, label_axes=True,
                       plot_measurement=True, plot_best_fit=True, plot_initial_fit=False, plot_resonance=True,
                       measurement_settings=None, best_fit_settings=None, initial_fit_settings=None,
                       resonance_settings=None, **subplots_kwds):
    if axes is None:
        figure, axes = plt.subplots(**subplots_kwds)
    else:
        figure = None
    if plot_measurement:
        measurement_kwds = measurement_defaults.copy()
        if measurement_settings is not None:
            measurement_kwds.update(measurement_settings)
        if normalize:
            measurement_data = resonator.foreground_data
        else:
            measurement_data = resonator.data
        axes.plot(frequency_scale * resonator.frequency, scaler(measurement_data), **measurement_kwds)
    if plot_best_fit or plot_initial_fit:  # Used for both best-fit and initial-fit plots
        if num_model_points is None:
            model_frequency = resonator.frequency
        else:
            model_frequency = np.linspace(resonator.frequency.min(), resonator.frequency.max(), num_model_points)
    if plot_best_fit:
        best_fit_kwds = best_fit_defaults.copy()
        if best_fit_settings is not None:
            best_fit_kwds.update(best_fit_settings)
        if normalize:
            best_fit_data = resonator.evaluate_fit_foreground(frequency=model_frequency)
        else:
            best_fit_data = resonator.evaluate_fit(frequency=model_frequency)
        axes.plot(frequency_scale * model_frequency, scaler(best_fit_data), **best_fit_kwds)
        if plot_resonance:
            best_fit_resonance_kwds = best_fit_defaults.copy()
            best_fit_resonance_kwds.update(resonance_defaults)
            if resonance_settings is not None:
                best_fit_resonance_kwds.update(resonance_settings)
            if normalize:
                best_fit_resonance = resonator.evaluate_fit_foreground(frequency=resonator.resonance_frequency)
            else:
                best_fit_resonance = resonator.evaluate_fit(frequency=resonator.resonance_frequency)
            axes.plot(frequency_scale * resonator.resonance_frequency, scaler(best_fit_resonance),
                      **best_fit_resonance_kwds)
    if plot_initial_fit:
        initial_fit_kwds = initial_fit_defaults.copy()
        if initial_fit_settings is not None:
            initial_fit_kwds.update(initial_fit_settings)
        if normalize:
            initial_fit_data = resonator.evaluate_initial_foreground(frequency=model_frequency)
        else:
            initial_fit_data = resonator.evaluate_initial(frequency=model_frequency)
        axes.plot(frequency_scale * model_frequency, scaler(initial_fit_data), **initial_fit_kwds)
        if plot_resonance:
            initial_fit_resonance_kwds = initial_fit_defaults.copy()
            initial_fit_resonance_kwds.update(resonance_defaults)
            if resonance_settings is not None:
                initial_fit_resonance_kwds.update(resonance_settings)
            if normalize:
                initial_fit_resonance = resonator.evaluate_initial_foreground(frequency=resonator.resonance_frequency)
            else:
                initial_fit_resonance = resonator.evaluate_initial(frequency=resonator.resonance_frequency)
            axes.plot(frequency_scale * resonator.resonance_frequency, scaler(initial_fit_resonance),
                      **initial_fit_resonance_kwds)
    if three_ticks:
        axes.set_xticks(frequency_scale * np.array([resonator.frequency.min(), resonator.resonance_frequency,
                                                    resonator.frequency.max()]))
    if label_axes:
        try:
            axes.set_xlabel('frequency / {}'.format(frequency_scale_to_unit[frequency_scale]))
        except KeyError:
            axes.set_xlabel('frequency')
        axes.set_ylabel(vertical_label)
    if figure is not None:
        return figure, axes


def real_and_imaginary(resonator, axes=None, normalize=False, num_model_points=default_num_model_points,
                       equal_aspect=True, label_axes=True, plot_measurement=True, plot_best_fit=True,
                       plot_initial_fit=False, plot_resonance=True, measurement_settings=None, best_fit_settings=None,
                       initial_fit_settings=None, resonance_settings=None, **subplots_kwds):
    """
    Plot imaginary parts versus real parts on the given axis for the data, best-fit model, and model at the best-fit
    resonance frequency; return a structure containing the measurement, model, and resonance values.

    :param resonator: an instance of a fitter.ResonatorFitter subclass.
    :param axes: a matplotlib Axes instance.
    :param normalize: if True, normalize all of the plotted values to the resonator plane by dividing them by the
      best-fit background model values.
    :param num_model_points: the number of points at which to evaluate the model over the measurement frequency range.
    :param equal_aspect: if True, set the axes aspect ratio to 'equal' so that the normalized resonance forms a circle.
    :param label_axes: if True, give the axes reasonable labels.
    :param plot_measurement: if True, plot the measured data.
    :param plot_best_fit: if True, plot the best-fit model.
    :param plot_initial_fit: if True, plot the initial-fit model.
    :param plot_resonance: if True, plot the best-fit and/or initial-fit model data at the corresponding resonance
      frequency.
    :param measurement_settings: a dict of pyplot.plot keywords used to plot the measurement values; see
      `measurement_defaults` in this module.
    :param best_fit_settings: a dict of pyplot.plot keywords used to plot the best-fit model values; see
    `best_fit_defaults` in this module.
    :param initial_fit_settings: a dict of pyplot.plot keywords used to plot the initial-fit modle values; see
      `initial_fit_defaults` in this module.
    :param resonance_settings: a dict of pyplot.plot keywords used to plot the best-fit and/or initial-fit values at the
      corresponding resonance frequency(ies); see `resonance_defaults` in this module.
    :return: if axes is None, return a new Figure and Axes objects; otherwise, return None.
    """
    if axes is None:
        figure, axes = plt.subplots(**subplots_kwds)
    else:
        figure = None
    if plot_measurement:
        measurement_kwds = measurement_defaults.copy()
        if measurement_settings is not None:
            measurement_kwds.update(measurement_settings)
        if normalize:
            measurement_data = resonator.foreground_data
        else:
            measurement_data = resonator.data
        axes.plot(measurement_data.real, measurement_data.imag, **measurement_kwds)
    if plot_best_fit or plot_initial_fit:  # Used for both best-fit and initial-fit plots
        if num_model_points is None:
            model_frequency = resonator.frequency
        else:
            model_frequency = np.linspace(resonator.frequency.min(), resonator.frequency.max(), num_model_points)
    if plot_best_fit:
        best_fit_kwds = best_fit_defaults.copy()
        if best_fit_settings is not None:
            best_fit_kwds.update(best_fit_settings)
        if normalize:
            best_fit_data = resonator.evaluate_fit_foreground(frequency=model_frequency)
        else:
            best_fit_data = resonator.evaluate_fit(frequency=model_frequency)
        axes.plot(best_fit_data.real, best_fit_data.imag, **best_fit_kwds)
        if plot_resonance:
            best_fit_resonance_kwds = best_fit_defaults.copy()
            best_fit_resonance_kwds.update(resonance_defaults)
            if resonance_settings is not None:
                best_fit_resonance_kwds.update(resonance_settings)
            if normalize:
                best_fit_resonance = resonator.evaluate_fit_foreground(frequency=resonator.resonance_frequency)
            else:
                best_fit_resonance = resonator.evaluate_fit(frequency=resonator.resonance_frequency)
            axes.plot(best_fit_resonance.real, best_fit_resonance.imag, **best_fit_resonance_kwds)
    if plot_initial_fit:
        initial_fit_kwds = initial_fit_defaults.copy()
        if initial_fit_settings is not None:
            initial_fit_kwds.update(initial_fit_settings)
        if normalize:
            initial_fit_data = resonator.evaluate_initial_foreground(frequency=model_frequency)
        else:
            initial_fit_data = resonator.evaluate_initial(frequency=model_frequency)
        axes.plot(initial_fit_data.real, initial_fit_data.imag, **initial_fit_kwds)
        if plot_resonance:
            initial_fit_resonance_kwds = initial_fit_defaults.copy()
            initial_fit_resonance_kwds.update(resonance_defaults)
            if resonance_settings is not None:
                initial_fit_resonance_kwds.update(resonance_settings)
            if normalize:
                initial_fit_resonance = resonator.evaluate_initial_foreground(
                    frequency=resonator.resonance_frequency)
            else:
                initial_fit_resonance = resonator.evaluate_initial(frequency=resonator.resonance_frequency)
            axes.plot(initial_fit_resonance.real, initial_fit_resonance.imag, **initial_fit_resonance_kwds)
    if equal_aspect:
        axes.set_aspect('equal')
    if label_axes:
        axes.set_xlabel('real')
        axes.set_ylabel('imag')
    if figure is not None:
        return figure, axes


def triptych(resonator, three_axes=None, normalize=False, num_model_points=default_num_model_points,
             frequency_scale=1, three_ticks=True, decibels=True, degrees=True, equal_aspect=True, label_axes=True,
             figure_settings=None, gridspec_settings=None, plot_measurement=True, plot_best_fit=True,
             plot_initial_fit=False, plot_resonance=True, measurement_settings=None, best_fit_settings=None,
             initial_fit_settings=None, resonance_settings=None):
    """
    Plot the resonator data in three ways: magnitude versus frequency, phase versus frequency, and imaginary versus real
    using the plotting functions in this module. See those functions for the meanings of the parameters not given below.

    :param three_axes: an iterable of three matplotlib Axes objects that will be used to plot the magnitude, phase, and
    complex data, in that order; if None, create and return a new Figure and three Axes objects.
    :figure_settings: keywords passed to pyplot.figure; ignored if axes is not None
    if axes is None, return a new Figure and three Axes objects; otherwise, return None.
    """
    if three_axes is None:
        figure_kwds = triptych_figure_defaults.copy()
        if figure_settings is not None:
            figure_kwds.update(figure_settings)
        figure = plt.figure(**figure_kwds)
        gridspec_kwds = triptych_gridspec_defaults.copy()
        if gridspec_settings is not None:
            gridspec_kwds.update(gridspec_settings)
        gridspec = plt.GridSpec(2, 2, **gridspec_kwds)
        ax_magnitude = figure.add_subplot(plt.subplot(gridspec.new_subplotspec((0, 0), 1, 1)))
        ax_phase = figure.add_subplot(plt.subplot(gridspec.new_subplotspec((1, 0), 1, 1)))
        ax_complex = figure.add_subplot(plt.subplot(gridspec.new_subplotspec((0, 1), 2, 1)))
        three_axes = (ax_magnitude, ax_phase, ax_complex)
    else:
        figure = None
        ax_magnitude, ax_phase, ax_complex = three_axes
    magnitude_vs_frequency(resonator=resonator, axes=ax_magnitude, normalize=normalize,
                           num_model_points=num_model_points, frequency_scale=frequency_scale, three_ticks=three_ticks,
                           decibels=decibels, label_axes=label_axes,
                           plot_measurement=plot_measurement, plot_best_fit=plot_best_fit,
                           plot_initial_fit=plot_initial_fit, plot_resonance=plot_resonance,
                           nmeasurement_settings=measurement_settings, best_fit_settings=best_fit_settings,
                           initial_fit_settings=initial_fit_settings, resonance_settings=resonance_settings)
    phase_vs_frequency(resonator=resonator, axes=ax_phase, normalize=normalize, num_model_points=num_model_points,
                       frequency_scale=frequency_scale, three_ticks=three_ticks, degrees=degrees, label_axes=label_axes,
                       plot_measurement=plot_measurement, plot_best_fit=plot_best_fit,
                       plot_initial_fit=plot_initial_fit, plot_resonance=plot_resonance,
                       nmeasurement_settings=measurement_settings, best_fit_settings=best_fit_settings,
                       initial_fit_settings=initial_fit_settings, resonance_settings=resonance_settings)
    real_and_imaginary(resonator=resonator, axes=ax_complex, normalize=normalize, num_model_points=num_model_points,
                       equal_aspect=equal_aspect, label_axes=label_axes,
                       plot_measurement=plot_measurement, plot_best_fit=plot_best_fit,
                       plot_initial_fit=plot_initial_fit, plot_resonance=plot_resonance,
                       nmeasurement_settings=measurement_settings, best_fit_settings=best_fit_settings,
                       initial_fit_settings=initial_fit_settings, resonance_settings=resonance_settings)
    if figure is not None:
        return figure, three_axes


def photon_number_vs_frequency(resonator, input_power_dBm, axes=None, num_model_points=default_num_model_points,
                               frequency_scale=1, three_ticks=True, label_axes=True, plot_settings=None,
                               **subplots_kwds):
    if axes is None:
        figure, axes = plt.subplots(**subplots_kwds)
    else:
        figure = None
    if num_model_points is None:
        frequency = resonator.frequency.copy()
    else:
        frequency = np.linspace(resonator.frequency.min(), resonator.frequency.max(), num_model_points)
    plot_kwds = photon_number_defaults.copy()
    if plot_settings is not None:
        plot_kwds.update(plot_settings)
    photon_number = resonator.photon_number_from_power(input_frequency=frequency, input_power_dBm=input_power_dBm)
    axes.plot(frequency_scale * frequency, photon_number, **plot_kwds)
    if three_ticks:
        axes.set_xticks(frequency_scale * np.array([resonator.frequency.min(), resonator.resonance_frequency,
                                                    resonator.frequency.max()]))
    if label_axes:
        try:
            axes.set_xlabel('frequency / {}'.format(frequency_scale_to_unit[frequency_scale]))
        except KeyError:
            axes.set_xlabel('frequency')
        axes.set_ylabel("photon number")
    if figure is not None:
        return figure, axes
