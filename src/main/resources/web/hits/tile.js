window.addEventListener("xlrelease.load", function() {
    window.xlrelease.queryTileData(function(response) {
        const chart = echarts.init(document.getElementById('main'));
        const responsePath = '_source';
        const labels = ["2xx", "3xx", "4xx", "5xx", "1xx"]
        const colors = ['#01B322', '#EBE700', '#EBA200', '#EB0800', '#2B3AEB'];
        let max;

        const timestampKeyName = response.data.data.timestampKeyName;
        const responseKeyName = response.data.data.responseKeyName;
        let selectedTimespan = response.data.data.selectedTimespan;
        let rawData = response.data.data.rawData;

        function getDataSortedByResponse() {
            const data = rawData.hits.hits;
            return data.reduce((p, c) => {
                const responseGroup = getResponseGroup(_.get(c[responsePath], responseKeyName));
                if (responseGroup in p) {
                    p[responseGroup].push(c);
                } else {
                    p[responseGroup] = [c];
                }
                return p;
            }, {});
        }

        function getResponseGroup(responseNumber) {
            const num = Number(responseNumber);
            if (num >= 100 && num < 200) return '100';
            if (num >= 200 && num < 300) return '200';
            if (num >= 300 && num < 400) return '300';
            if (num >= 400 && num < 500) return '400';
            if (num >= 500 && num < 600) return '500';
            return 0;
        }

        function getTimePoints(granularity, format) {
            const {
                unitShort,
                units
            } = getTimeFormats(granularity);
            const data = rawData.hits.hits
                .map(hit => (hit[responsePath][timestampKeyName]))
                .sort((a, b) => customSort(a, b));
            const startDate = moment(data[0]).startOf(granularity);
            const endDate = moment(data[data.length - 1]).startOf(granularity);
            let timespan = endDate.diff(startDate, units);
            const timePoints = [];

            if (format) {
                timePoints.push(startDate.format(format));
                for (let i = 0; i < timespan; i++) {
                    timePoints.push(startDate.add(1, unitShort).format(format));
                }
            } else {
                timePoints.push(startDate.unix());
                for (let i = 0; i < timespan; i++) {
                    timePoints.push(startDate.add(1, unitShort).unix());
                }
            }
            return timePoints;
        }

        function filterDataByTime(data, granularity) {
            const timePoints = getTimePoints(granularity).map(time => ({
                time,
                value: 0
            }));
            data.forEach(hit => {
                const timestamp = moment(hit[responsePath][timestampKeyName]).startOf(granularity).unix();
                timePoints.find(m => m.time === timestamp).value++;
            });
            const currentMax = Math.round(_.maxBy(timePoints, 'value').value * 1.1);
            max = currentMax > max ? currentMax : max;
            return timePoints;
        }

        function getSeries() {
            const data = getDataSortedByResponse();
            return Object.keys(data).map((respRange, i) => {
                return {
                    name: `Hits ${labels[i]}`,
                    type: 'line',
                    smooth: false,
                    symbol: 'none',
                    sampling: 'average',
                    itemStyle: {
                        color: colors[i]
                    },
                    data: filterDataByTime(data[respRange], selectedTimespan).map(v => v.value)
                }
            });
        }

        function getTimeFormats(granularity) {
            switch (granularity) {
                case 'minute':
                    return {
                        unitShort: 'm',
                            units: 'minutes'
                    };
                case 'hour':
                    return {
                        unitShort: 'h',
                            units: 'hours'
                    };
                case 'day':
                    return {
                        unitShort: 'd',
                            units: 'days'
                    }
            }
        }

        function getChartOptions() {
            return {
                tooltip: {
                    trigger: 'axis',
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: getTimePoints(selectedTimespan, 'LLL')
                },
                yAxis: {
                    type: 'value',
                    boundaryGap: [0, '100%'],
                    min: 0,
                    max: max
                },
                dataZoom: [
                    {
                        type: 'inside',
                        start: 0,
                        end: 100
                    },
                    {
                        start: 0,
                        end: 100,
                        handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                        handleSize: '80%',
                        handleStyle: {
                            color: '#fff',
                            shadowBlur: 3,
                            shadowColor: 'rgba(0, 0, 0, 0.6)',
                            shadowOffsetX: 2,
                            shadowOffsetY: 2
                        },
                        left: '24%',
                        right: '24%'
                    }
                ],
                series: getSeries()
            };
        }

        function customSort(one, two) {
            if (one > two) return 1;
            return -1;
        }

        chart.setOption(getChartOptions());

        window.addEventListener('resize', () => {
            chart.resize();
        });
    });
});