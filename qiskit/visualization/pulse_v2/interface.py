# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Qiskit pulse drawer.

This module provides a common user interface for the pulse drawer.
The `draw` function takes a pulse program to visualize with a stylesheet and
backend information along with several control arguments.
The drawer canvas object is internally initialized from the input data and
the configured canvas is passed to the one of plotter APIs to generate visualization data.
"""

from typing import Union, Optional, Dict, Any, Tuple, List

from qiskit.providers import Backend
from qiskit.pulse import Waveform, SymbolicPulse, Schedule, ScheduleBlock
from qiskit.pulse.channels import Channel
from qiskit.visualization.exceptions import VisualizationError
from qiskit.visualization.pulse_v2 import core, device_info, stylesheet, types
from qiskit.exceptions import MissingOptionalLibraryError
from qiskit.utils import deprecate_arg


@deprecate_arg("show_barriers", new_alias="plot_barriers", since="1.1.0", pending=True)
def draw(
    program: Union[Waveform, SymbolicPulse, Schedule, ScheduleBlock],
    style: Optional[Dict[str, Any]] = None,
    backend: Optional[Backend] = None,
    time_range: Optional[Tuple[int, int]] = None,
    time_unit: str = types.TimeUnits.CYCLES.value,
    disable_channels: Optional[List[Channel]] = None,
    show_snapshot: bool = True,
    show_framechange: bool = True,
    show_waveform_info: bool = True,
    plot_barrier: bool = True,
    plotter: str = types.Plotter.Mpl2D.value,
    axis: Optional[Any] = None,
    show_barrier: bool = True,
):
    """Generate visualization data for pulse programs.

    Args:
        program: Program to visualize. This program can be arbitrary Qiskit Pulse program,
            such as :py:class:`~qiskit.pulse.Waveform`, :py:class:`~qiskit.pulse.SymbolicPulse`,
            :py:class:`~qiskit.pulse.Schedule` and :py:class:`~qiskit.pulse.ScheduleBlock`.
        style: Stylesheet options. This can be dictionary or preset stylesheet classes. See
            :py:class:`~qiskit.visualization.pulse_v2.stylesheets.IQXStandard`,
            :py:class:`~qiskit.visualization.pulse_v2.stylesheets.IQXSimple`, and
            :py:class:`~qiskit.visualization.pulse_v2.stylesheets.IQXDebugging` for details of
            preset stylesheets. See also the stylesheet section for details of configuration keys.
        backend: Backend object to play the input pulse program. If provided, the plotter
            may use to make the visualization hardware aware.
        time_range: Set horizontal axis limit. Tuple ``(tmin, tmax)``.
        time_unit: The unit of specified time range either ``dt`` or ``ns``.
            The unit of ``ns`` is available only when ``backend`` object is provided.
        disable_channels: A control property to show specific pulse channel.
            Pulse channel instances provided as a list is not shown in the output image.
        show_snapshot: Show snapshot instructions.
        show_framechange: Show frame change instructions. The frame change represents
            instructions that modulate phase or frequency of pulse channels.
        show_waveform_info: Show waveform annotations, i.e. name, of waveforms.
            Set ``True`` to show additional information about waveforms.
        plot_barrier: Show barrier lines.
        plotter: Name of plotter API to generate an output image.
            One of following APIs should be specified::

                mpl2d: Matplotlib API for 2D image generation.
                    Matplotlib API to generate 2D image. Charts are placed along y axis with
                    vertical offset. This API takes matplotlib.axes.Axes as `axis` input.

            `axis` and `style` kwargs may depend on the plotter.
        axis: Arbitrary object passed to the plotter. If this object is provided,
            the plotters use a given ``axis`` instead of internally initializing
            a figure object. This object format depends on the plotter.
            See plotter argument for details.
        show_barrier: DEPRECATED. Show barrier lines.

    Returns:
        Visualization output data.
        The returned data type depends on the `plotter`.
        If matplotlib family is specified, this will be a `matplotlib.pyplot.Figure` data.
        The returned data is generated by the :meth:`get_image` method of the specified plotter API.

    .. _style-dict-doc:

    **Style Dict Details**

    The stylesheet kwarg contains numerous options that define the style of the
    output pulse visualization.
    The stylesheet options can be classified into `formatter`, `generator` and `layout`.
    Those options available in the stylesheet are defined below:

    Args:
        formatter.general.fig_width: Width of output image (default `13`).
        formatter.general.fig_chart_height: Height of output image per chart.
            The height of each chart is multiplied with this factor and the
            sum of all chart heights becomes the height of output image (default `1.5`).
        formatter.general.vertical_resolution: Vertical resolution of the pulse envelope.
            The change of data points below this limit is ignored (default `1e-6`).
        formatter.general.max_scale: Maximum scaling factor of each chart. This factor is
            considered when chart auto-scaling is enabled (default `100`).
        formatter.color.waveforms: A dictionary of the waveform colors to use for
            each element type in the output visualization. The default values are::

                {
                    'W': `['#648fff', '#002999']`,
                    'D': `['#648fff', '#002999']`,
                    'U': `['#ffb000', '#994A00']`,
                    'M': `['#dc267f', '#760019']`,
                    'A': `['#dc267f', '#760019']`
                }

        formatter.color.baseline: Color code of lines of zero line of each chart
            (default `'#000000'`).
        formatter.color.barrier: Color code of lines of barrier (default `'#222222'`).
        formatter.color.background: Color code of the face color of canvas
            (default `'#f2f3f4'`).
        formatter.color.fig_title: Color code of the figure title text
            (default `'#000000'`).
        formatter.color.annotate: Color code of annotation texts in the canvas
            (default `'#222222'`).
        formatter.color.frame_change: Color code of the symbol for frame changes
            (default `'#000000'`).
        formatter.color.snapshot: Color code of the symbol for snapshot
            (default `'#000000'`)
        formatter.color.opaque_shape: Color code of the face and edge of opaque shape box
            (default `['#fffacd', '#000000']`)
        formatter.color.axis_label: Color code of axis labels (default `'#000000'`).
        formatter.alpha.fill_waveform: Transparency of waveforms. A value in the range from
            `0` to `1`. The value `0` gives completely transparent waveforms (default `0.3`).
        formatter.alpha.baseline: Transparency of base lines. A value in the range from
            `0` to `1`. The value `0` gives completely transparent base lines (default `1.0`).
        formatter.alpha.barrier: Transparency of barrier lines. A value in the range from
            `0` to `1`. The value `0` gives completely transparent barrier lines (default `0.7`).
        formatter.alpha.opaque_shape: Transparency of opaque shape box. A value in the range from
            `0` to `1`. The value `0` gives completely transparent barrier lines (default `0.7`).
        formatter.layer.fill_waveform: Layer index of waveforms. Larger number comes
            in the front of the output image (default `2`).
        formatter.layer.baseline: Layer index of baselines. Larger number comes
            in the front of the output image (default `1`).
        formatter.layer.barrier: Layer index of barrier lines. Larger number comes
            in the front of the output image (default `1`).
        formatter.layer.annotate: Layer index of annotations. Larger number comes
            in the front of the output image (default `5`).
        formatter.layer.axis_label: Layer index of axis labels. Larger number comes
            in the front of the output image (default `5`).
        formatter.layer.frame_change: Layer index of frame change symbols. Larger number comes
            in the front of the output image (default `4`).
        formatter.layer.snapshot: Layer index of snapshot symbols. Larger number comes
            in the front of the output image (default `3`).
        formatter.layer.fig_title: Layer index of the figure title. Larger number comes
            in the front of the output image (default `6`).
        formatter.margin.top: Margin from the top boundary of the figure canvas to
            the surface of the first chart (default `0.5`).
        formatter.margin.bottom: Margin from the bottom boundary of the figure canvas to
            the surface of the last chart (default `0.5`).
        formatter.margin.left_percent: Margin from the left boundary of the figure canvas to
            the zero point of the horizontal axis. The value is in units of percentage of
            the whole program duration. If the duration is 100 and the value of 0.5 is set,
            this keeps left margin of 5 (default `0.05`).
        formatter.margin.right_percent: Margin from the right boundary of the figure canvas to
            the left limit of the horizontal axis. The value is in units of percentage of
            the whole program duration. If the duration is 100 and the value of 0.5 is set,
            this keeps right margin of 5 (default `0.05`).
        formatter.margin.between_channel: Vertical margin between charts (default `0.2`).
        formatter.label_offset.pulse_name: Offset of pulse name annotations from the
            chart baseline (default `0.3`).
        formatter.label_offset.chart_info: Offset of chart info annotations from the
            chart baseline (default `0.3`).
        formatter.label_offset.frame_change: Offset of frame change annotations from the
            chart baseline (default `0.3`).
        formatter.label_offset.snapshot: Offset of snapshot annotations from the
            chart baseline (default `0.3`).
        formatter.text_size.axis_label: Text size of axis labels (default `15`).
        formatter.text_size.annotate: Text size of annotations (default `12`).
        formatter.text_size.frame_change: Text size of frame change symbols (default `20`).
        formatter.text_size.snapshot: Text size of snapshot symbols (default `20`).
        formatter.text_size.fig_title: Text size of the figure title (default `15`).
        formatter.text_size.axis_break_symbol: Text size of axis break symbols (default `15`).
        formatter.line_width.fill_waveform: Line width of the fringe of filled waveforms
            (default `0`).
        formatter.line_width.axis_break: Line width of axis breaks.
            The axis break line paints over other drawings with the background
            face color (default `6`).
        formatter.line_width.baseline: Line width of base lines (default `1`)
        formatter.line_width.barrier: Line width of barrier lines (default `1`).
        formatter.line_width.opaque_shape: Line width of opaque shape box (default `1`).
        formatter.line_style.fill_waveform: Line style of the fringe of filled waveforms. This
            conforms to the line style spec of matplotlib (default `'-'`).
        formatter.line_style.baseline: Line style of base lines. This
            conforms to the line style spec of matplotlib (default `'-'`).
        formatter.line_style.barrier: Line style of barrier lines. This
            conforms to the line style spec of matplotlib (default `':'`).
        formatter.line_style.opaque_shape: Line style of opaque shape box. This
            conforms to the line style spec of matplotlib (default `'--'`).
        formatter.channel_scaling.drive: Default scaling value of drive channel
            waveforms (default `1.0`).
        formatter.channel_scaling.control: Default scaling value of control channel
            waveforms (default `1.0`).
        formatter.channel_scaling.measure: Default scaling value of measure channel
            waveforms (default `1.0`).
        formatter.channel_scaling.acquire: Default scaling value of acquire channel
            waveforms (default `1.0`).
        formatter.channel_scaling.pos_spacing: Minimum height of chart above the baseline.
            Chart top is determined based on the maximum height of waveforms associated
            with the chart. If the maximum height is below this value, this value is set
            as the chart top (default 0.1).
        formatter.channel_scaling.neg_spacing: Minimum height of chart below the baseline.
            Chart bottom is determined based on the minimum height of waveforms associated
            with the chart. If the minimum height is above this value, this value is set
            as the chart bottom (default -0.1).
        formatter.box_width.opaque_shape: Default box length of the waveform representation
            when the instruction is parameterized and duration is not bound or not defined.
            Value is units in dt (default: 150).
        formatter.box_height.opaque_shape: Default box height of the waveform representation
            when the instruction is parameterized (default: 0.4).
        formatter.axis_break.length: Waveform or idle time duration that axis break is
            applied. Intervals longer than this value are truncated.
            The value is in units of data points (default `3000`).
        formatter.axis_break.max_length: Length of new waveform or idle time duration
            after axis break is applied. Longer intervals are truncated to this length
            (default `1000`).
        formatter.control.fill_waveform: Set `True` to fill waveforms with face color
            (default `True`). When you disable this option, you should set finite line width
            to `formatter.line_width.fill_waveform`, otherwise nothing will appear in the graph.
        formatter.control.apply_phase_modulation: Set `True` to apply phase modulation
            to the waveforms (default `True`).
        formatter.control.show_snapshot_channel: Set `True` to show snapshot instructions
            (default `True`).
        formatter.control.show_acquire_channel: Set `True` to show acquire channels
            (default `True`).
        formatter.control.show_empty_channel: Set `True` to show charts without any waveforms
            (default `True`).
        formatter.control.auto_chart_scaling: Set `True` to apply auto-scaling to charts
            (default `True`).
        formatter.control.axis_break: Set `True` to apply axis break for long intervals
            (default `True`).
        formatter.unicode_symbol.frame_change: Text that represents the symbol of
            frame change. This text is used when the plotter doesn't support latex
            (default u'\u21BA').
        formatter.unicode_symbol.snapshot: Text that represents the symbol of
            snapshot. This text is used when the plotter doesn't support latex
            (default u'\u21AF').
        formatter.unicode_symbol.phase_parameter: Text that represents the symbol of
            parameterized phase value. This text is used when the plotter doesn't support latex
            (default u'\u03b8').
        formatter.unicode_symbol.freq_parameter: Text that represents the symbol of
            parameterized frequency value. This text is used when the plotter doesn't support latex
            (default 'f').
        formatter.latex_symbol.frame_change: Latex text that represents the symbol of
            frame change (default r'\\circlearrowleft').
        formatter.latex_symbol.snapshot: Latex text that represents the symbol of
            snapshot (default '').
        formatter.latex_symbol.phase_parameter: Latex text that represents the symbol of
            parameterized phase value (default r'\theta').
        formatter.latex_symbol.freq_parameter: Latex text that represents the symbol of
            parameterized frequency value (default 'f').
        generator.waveform: List of callback functions that generates drawing
            for waveforms. Arbitrary callback functions satisfying the generator format
            can be set here. There are some default generators in the pulse drawer.
            See :py:mod:`~qiskit.visualization.pulse_v2.generators.waveform` for more details.
            No default generator is set.
        generator.frame: List of callback functions that generates drawing
            for frame changes. Arbitrary callback functions satisfying the generator format
            can be set here. There are some default generators in the pulse drawer.
            See :py:mod:`~qiskit.visualization.pulse_v2.generators.frame` for more details.
            No default generator is set.
        generator.chart: List of callback functions that generates drawing
            for charts. Arbitrary callback functions satisfying the generator format
            can be set here. There are some default generators in the pulse drawer.
            See :py:mod:`~qiskit.visualization.pulse_v2.generators.chart` for more details.
            No default generator is set.
        generator.snapshot: List of callback functions that generates drawing
            for snapshots. Arbitrary callback functions satisfying the generator format
            can be set here. There are some default generators in the pulse drawer.
            See :py:mod:`~qiskit.visualization.pulse_v2.generators.snapshot` for more details.
            No default generator is set.
        generator.barrier: List of callback functions that generates drawing
            for barriers. Arbitrary callback functions satisfying the generator format
            can be set here. There are some default generators in the pulse drawer.
            See :py:mod:`~qiskit.visualization.pulse_v2.generators.barrier` for more details.
            No default generator is set.
        layout.chart_channel_map: Callback function that determines the relationship
            between pulse channels and charts.
            See :py:mod:`~qiskit.visualization.pulse_v2.layout` for more details.
            No default layout is set.
        layout.time_axis_map: Callback function that determines the layout of
            horizontal axis labels.
            See :py:mod:`~qiskit.visualization.pulse_v2.layout` for more details.
            No default layout is set.
        layout.figure_title: Callback function that generates a string for
            the figure title.
            See :py:mod:`~qiskit.visualization.pulse_v2.layout` for more details.
            No default layout is set.

    Examples:
        To visualize a pulse program, you can call this function with set of
        control arguments. Most of appearance of the output image can be controlled by the
        stylesheet.

        Drawing with the default stylesheet.

        .. plot::
           :include-source:

            from qiskit import QuantumCircuit, transpile, schedule
            from qiskit.visualization.pulse_v2 import draw
            from qiskit.providers.fake_provider import GenericBackendV2

            qc = QuantumCircuit(2)
            qc.h(0)
            qc.cx(0, 1)
            qc.measure_all()
            qc = transpile(qc, GenericBackendV2(5), layout_method='trivial')
            sched = schedule(qc, GenericBackendV2(5))

            draw(sched, backend=GenericBackendV2(5))

        Drawing with the stylesheet suited for publication.

        .. plot::
           :include-source:

            from qiskit import QuantumCircuit, transpile, schedule
            from qiskit.visualization.pulse_v2 import draw, IQXSimple
            from qiskit.providers.fake_provider import GenericBackendV2

            qc = QuantumCircuit(2)
            qc.h(0)
            qc.cx(0, 1)
            qc.measure_all()
            qc = transpile(qc, GenericBackendV2(5), layout_method='trivial')
            sched = schedule(qc, GenericBackendV2(5))

            draw(sched, style=IQXSimple(), backend=GenericBackendV2(5))

        Drawing with the stylesheet suited for program debugging.

        .. plot::
           :include-source:

            from qiskit import QuantumCircuit, transpile, schedule
            from qiskit.visualization.pulse_v2 import draw, IQXDebugging
            from qiskit.providers.fake_provider import GenericBackendV2

            qc = QuantumCircuit(2)
            qc.h(0)
            qc.cx(0, 1)
            qc.measure_all()
            qc = transpile(qc, GenericBackendV2(5), layout_method='trivial')
            sched = schedule(qc, GenericBackendV2(5))

            draw(sched, style=IQXDebugging(), backend=GenericBackendV2(5))

        You can partially customize a preset stylesheet when initializing it.

        .. plot::
           :include-source:
           :nofigs:

            my_style = {
                'formatter.channel_scaling.drive': 5,
                'formatter.channel_scaling.control': 1,
                'formatter.channel_scaling.measure': 5
            }
            style = IQXStandard(**my_style)
            # draw
            draw(sched, style=style, backend=GenericBackendV2(5))

        In the same way as above, you can create custom generator or layout functions
        and update the existing stylesheet with custom functions.
        This feature enables you to customize most of the appearance of the output image
        without modifying the codebase.

    Raises:
        MissingOptionalLibraryError: When required visualization package is not installed.
        VisualizationError: When invalid plotter API or invalid time range is specified.
    """
    del show_barrier
    temp_style = stylesheet.QiskitPulseStyle()
    temp_style.update(style or stylesheet.IQXStandard())

    if backend:
        device = device_info.OpenPulseBackendInfo.create_from_backend(backend)
    else:
        device = device_info.OpenPulseBackendInfo()

    # create empty canvas and load program
    canvas = core.DrawerCanvas(stylesheet=temp_style, device=device)
    canvas.load_program(program=program)

    #
    # update configuration
    #

    # time range
    if time_range:
        if time_unit == types.TimeUnits.CYCLES.value:
            canvas.set_time_range(*time_range, seconds=False)
        elif time_unit == types.TimeUnits.NS.value:
            canvas.set_time_range(*time_range, seconds=True)
        else:
            raise VisualizationError(f"Invalid time unit {time_unit} is specified.")

    # channels not shown
    if disable_channels:
        for chan in disable_channels:
            canvas.set_disable_channel(chan, remove=True)

    # show snapshots
    if not show_snapshot:
        canvas.set_disable_type(types.SymbolType.SNAPSHOT, remove=True)
        canvas.set_disable_type(types.LabelType.SNAPSHOT, remove=True)

    # show frame changes
    if not show_framechange:
        canvas.set_disable_type(types.SymbolType.FRAME, remove=True)
        canvas.set_disable_type(types.LabelType.FRAME, remove=True)

    # show waveform info
    if not show_waveform_info:
        canvas.set_disable_type(types.LabelType.PULSE_INFO, remove=True)
        canvas.set_disable_type(types.LabelType.PULSE_NAME, remove=True)

    # show barrier
    if not plot_barrier:
        canvas.set_disable_type(types.LineType.BARRIER, remove=True)

    canvas.update()

    #
    # Call plotter API and generate image
    #

    if plotter == types.Plotter.Mpl2D.value:
        try:
            from qiskit.visualization.pulse_v2.plotters import Mpl2DPlotter
        except ImportError as ex:
            raise MissingOptionalLibraryError(
                libname="Matplotlib",
                name="plot_histogram",
                pip_install="pip install matplotlib",
            ) from ex
        plotter_api = Mpl2DPlotter(canvas=canvas, axis=axis)
        plotter_api.draw()
    else:
        raise VisualizationError(f"Plotter API {plotter} is not supported.")

    return plotter_api.get_image()
