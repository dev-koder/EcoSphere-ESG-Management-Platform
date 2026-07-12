/** @odoo-module **/

import { Component } from "@odoo/owl";

export class LeaderboardWidget extends Component {}

LeaderboardWidget.template = "ecosphere_esg.LeaderboardWidget";
LeaderboardWidget.props = {
    leaderboard: { type: Array, default: () => [] }
};
