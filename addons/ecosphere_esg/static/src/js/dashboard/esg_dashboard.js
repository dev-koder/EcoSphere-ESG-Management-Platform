/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState, useEffect, useRef } from "@odoo/owl";
import { LeaderboardWidget } from "./leaderboard_widget";

export class EsgDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            data: {
                overall_score: 0,
                avg_env: 0,
                avg_soc: 0,
                avg_gov: 0,
                department_scores: [],
                leaderboard: [],
                carbon_trend: {}
            },
        });
        this.chartRef = useRef("deptChart");
        this.trendRef = useRef("trendChart");

        onWillStart(async () => {
            this.state.data = await this.orm.call("esg.department.score", "get_dashboard_data", []);
        });

        useEffect(() => {
            this.renderCharts();
        });
    }

    renderCharts() {
        if (this.chartRef.el) {
            const labels = this.state.data.department_scores.map(d => d.department);
            const data = this.state.data.department_scores.map(d => d.total_score);
            
            new Chart(this.chartRef.el, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Total ESG Score',
                        data: data,
                        backgroundColor: '#1f77b4'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true, max: 100 } }
                }
            });
        }
        
        if (this.trendRef.el) {
            const labels = Object.keys(this.state.data.carbon_trend);
            const data = Object.values(this.state.data.carbon_trend);
            
            new Chart(this.trendRef.el, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Carbon Emissions (tCO2e)',
                        data: data,
                        borderColor: '#d62728',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }
}

EsgDashboard.template = "ecosphere_esg.Dashboard";
EsgDashboard.components = { LeaderboardWidget };

registry.category("actions").add("ecosphere_esg.dashboard", EsgDashboard);
