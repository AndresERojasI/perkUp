/**
 * @namespace Chart
 */
var Chart = require('./web_core/web_core.js')();

require('./web_core/web_core.helpers')(Chart);
require('./web_core/web_core.canvasHelpers')(Chart);
require('./web_core/web_core.element')(Chart);
require('./web_core/web_core.animation')(Chart);
require('./web_core/web_core.controller')(Chart);
require('./web_core/web_core.datasetController')(Chart);
require('./web_core/web_core.layoutService')(Chart);
require('./web_core/web_core.scaleService')(Chart);
require('./web_core/web_core.plugin.js')(Chart);
require('./web_core/web_core.ticks.js')(Chart);
require('./web_core/web_core.scale')(Chart);
require('./web_core/web_core.title')(Chart);
require('./web_core/web_core.legend')(Chart);
require('./web_core/web_core.interaction')(Chart);
require('./web_core/web_core.tooltip')(Chart);

require('./elements/element.arc')(Chart);
require('./elements/element.line')(Chart);
require('./elements/element.point')(Chart);
require('./elements/element.rectangle')(Chart);

require('./scales/scale.linearbase.js')(Chart);
require('./scales/scale.category')(Chart);
require('./scales/scale.linear')(Chart);
require('./scales/scale.logarithmic')(Chart);
require('./scales/scale.radialLinear')(Chart);
require('./scales/scale.time')(Chart);

// Controllers must be loaded after elements
// See Chart.web_core.datasetController.dataElementType
require('./controllers/controller.bar')(Chart);
require('./controllers/controller.bubble')(Chart);
require('./controllers/controller.doughnut')(Chart);
require('./controllers/controller.line')(Chart);
require('./controllers/controller.polarArea')(Chart);
require('./controllers/controller.radar')(Chart);

require('./charts/Chart.Bar')(Chart);
require('./charts/Chart.Bubble')(Chart);
require('./charts/Chart.Doughnut')(Chart);
require('./charts/Chart.Line')(Chart);
require('./charts/Chart.PolarArea')(Chart);
require('./charts/Chart.Radar')(Chart);
require('./charts/Chart.Scatter')(Chart);

window.Chart = module.exports = Chart;
