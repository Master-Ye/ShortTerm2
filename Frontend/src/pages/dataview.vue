<template>
  <div class="q-pa-md row items-start q-gutter-md" style="width: 1275px">
    <q-card
      class="my-card"
      flat
      bordered
      style="width: 1700px; background-color: #161627"
    >
      <q-item>
        <q-item-section>
          <q-item-label style="color: white" class="font-bold">行业图表统计</q-item-label>
          <q-item-label style="color: white" caption> Subhead </q-item-label>
        </q-item-section>
      </q-item>
      <q-separator vertical />
      <q-card-section>
        <q-card-section col-5 flex flex-center class="inline-block">
          <v-chart class="chart" :option="option" autoresize />
        </q-card-section>
        <q-card-section class="inline-block">
          <v-chart class="chart" :option="option1" autoresize />
        </q-card-section>
      </q-card-section>
    </q-card>

    <q-card
      class="my-card"
      flat
      bordered
      style="width: 1700px; background-color: #161627"
    >
      <q-item>
        <q-item-section>
          <q-item-label style="color: white" class="font-bold">区域图表统计</q-item-label>
          <q-item-label style="color: white" caption> Subhead </q-item-label>
        </q-item-section>
      </q-item>
      <q-separator vertical />
      <q-card-section>
        <q-card-section col-5 flex flex-center class="inline-block">
          <v-chart class="chart" :option="option2" autoresize />
        </q-card-section>
        <q-card-section class="inline-block">
          <v-chart class="chart" :option="option3" autoresize />
        </q-card-section>
      </q-card-section>
    </q-card>
  </div>
</template>
<script setup>
import * as echarts from "echarts";
import axios from "axios";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import { TitleComponent, TooltipComponent, LegendComponent } from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, provide } from "vue";
import { onMounted } from "vue";
const viewdata = ref([]);
onMounted(() => {
  axios.get("http://localhost:5000/viewdata").then((res) => {
    console.log(res.data);
    viewdata.value = res.data;
    console.log(viewdata.value);
    let temp1 = viewdata.value.filter((item) => item.ss == 1);
    const industryCount = {};
    const locationCount = {};
    console.log(temp1);
    for (const item of temp1) {
      const industry = item.industry;
      if (industry in industryCount) {
        industryCount[industry] += 1;
      } else {
        industryCount[industry] = 1;
      }
    }
    console.log(industryCount);
    for (const item of temp1) {
      const location = item.location;
      if (location in locationCount) {
        locationCount[location] += 1;
      } else {
        locationCount[location] = 1;
      }
    }
    const result = option.value.xAxis.data.map(
      (industry) => industryCount[industry] || 0
    );

    const result1 = option2.value.xAxis.data.map(
      (location) => locationCount[location] || 0
    );
    option.value.series[0].data = result;
    console.log(result);
    option2.value.series[0].data = result1;
    for (let i = 0; i < result.length; i++) {
      option1.value.series[0].data[i].value = result[i];
      decount.value += result[i];
      option3.value.title[1].subtext = option1.value.title[1].subtext = decount.value;
    }
    for (let i = 0; i < result1.length; i++) {
      option3.value.series[0].data[i].value = result1[i];
      decount.value += result1[i];
    }
  });
});
const decount = ref(0);
const option1 = ref({
  backgroundColor: "#161627",
  title: [
    {
      // text: '标题',
      textStyle: {
        fontSize: 18,
        color: "black",
      },
      left: "2%",
    },
    {
      text: "当前违约" + "\n" + "总人数",
      subtext: 500,
      textStyle: {
        fontSize: 19,
        color: "#FFA951",
        fontWeight: "normal",
      },
      subtextStyle: {
        fontSize: 19,
        color: "#fff",
        // fontWeight: 'bold'
      },
      textAlign: "center",
      x: "48%",
      y: "40%",
    },
  ],

  tooltip: {
    trigger: "item",
    formatter: function (parms) {
      // var str =  parms.seriesName+"</br>"+
      var str =
        parms.marker +
        "" +
        parms.data.legendname +
        "</br>" +
        "数量：" +
        parms.data.value +
        " 个</br>" +
        "占比：" +
        parms.percent +
        "%";
      return str;
    },
  },

  series: [
    {
      name: "标题",
      type: "pie",
      center: ["50%", "50%"],
      radius: ["40%", "50%"],
      clockwise: false, //饼图的扇区是否是顺时针排布
      avoidLabelOverlap: false,
      itemStyle: {
        borderColor: "#0d035c",
        borderWidth: 5,
      },
      label: {
        normal: {
          fontSize: 18,
          color: "#fff",
          formatter: function (params) {
            console.log(params, "params");
            var str = "";
            switch (params.name) {
              case "信息服务行业":
                str = "{a|" + params.value + "人}\n";
                break;
              case "化工行业":
                str = "{b|" + params.value + "人}\n";
                break;
              case "建筑行业":
                str = "{e|" + params.value + "人}\n";
                break;
              case "运输行业":
                str = "{d|" + params.value + "人}\n";
                break;
              case "食品行业":
                str = "{c|" + params.value + "人}\n";
                break;
            }
            return str;
          },
          rich: {
            a: {
              fontSize: 18,
              color: "#03c781",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            b: {
              fontSize: 18,
              color: "#03acd1",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            c: {
              fontSize: 18,
              color: "#ff7708",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            d: {
              fontSize: 18,
              color: "#0055ff",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            e: {
              fontSize: 18,
              color: "#96b497",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            nameStyle: {
              fontSize: 16,
              color: "#555",
              align: "left",
            },
            rate: {
              fontSize: 20,
              color: "#1ab4b8",
              align: "left",
            },
          },
          padding: [0, -10],
          // height: 35
        },
      },
      labelLine: {
        show: true,
        length: 20,
        length2: 35,
        smooth: false,
      },
      data: [
        {
          value: 80,
          legendname: "信息服务行业",
          name: "信息服务行业",
          itemStyle: { color: "#03acd1" },
        },
        {
          value: 150,
          legendname: "化工行业",
          name: "化工行业",
          itemStyle: { color: "#03c781" },
        },
        {
          value: 45,
          legendname: "建筑行业",
          name: "建筑行业",
          itemStyle: { color: "#96b497" },
        },
        {
          value: 150,
          legendname: "运输行业",
          name: "运输行业",
          itemStyle: { color: "#0055ff" },
        },
        {
          value: 150,
          legendname: "食品行业",
          name: "食品行业",
          itemStyle: { color: "#ff7708" },
        },
      ],
      z: 9,
    },
    {
      center: ["50%", "50%"], //仪表的位置
      name: "刻度", //仪表的名字
      type: "gauge", //统计图类型为仪表
      radius: 160, //统计图的半径大小
      min: 0, //最小刻度
      max: 100, //最大刻度
      splitNumber: 9, //刻度数量
      startAngle: 1, //开始刻度的角度
      endAngle: 360, //结束刻度的角度
      axisLine: {
        //设置默认刻度盘上的刻度不显示，重新定义刻度盘
        show: false,
        lineStyle: {
          width: 1,
          color: [[1, "rgba(255,255,255,0)"]],
        },
      }, //仪表盘轴线
      axisLabel: {
        //仪表盘上的数据
        show: false,
        color: "#4d5bd1", //仪表盘上的轴线颜色
        distance: 2, //图形与刻度的间距
      }, //刻度标签。
      axisTick: {
        show: true,
        splitNumber: 6, //刻度的段落数
        lineStyle: {
          color: "#00FCF7",
          width: 1, //刻度的宽度
          shadowColor: "#67FFFC",
          shadowBlur: 2,
        },
        length: 8, //刻度的长度
      }, //刻度样式
      pointer: {
        //表盘上的指针
        show: false,
      },
      itemStyle: {
        color: "#18c8ff",
      },

      splitLine: {
        //文字和刻度的偏移量
        show: true,
        length: 15, //便宜的长度
        lineStyle: {
          color: "#00FCF7",
          width: 4,
          shadowColor: "#67FFFC",
          shadowBlur: 4,
        },
      }, //分隔线样式
      z: 1,
    },
    {
      center: ["50%", "50%"], //仪表的位置
      name: "刻度", //仪表的名字
      type: "gauge", //统计图类型为仪表
      radius: 100, //统计图的半径大小
      min: 0, //最小刻度
      max: 100, //最大刻度
      splitNumber: 9, //刻度数量
      startAngle: 0, //开始刻度的角度
      endAngle: 360, //结束刻度的角度
      axisLine: {
        //设置默认刻度盘上的刻度不显示，重新定义刻度盘
        show: false,
        lineStyle: {
          width: 1,
          color: [[1, "rgba(255,255,255,0)"]],
        },
      }, //仪表盘轴线
      axisLabel: {
        //仪表盘上的数据
        show: false,
        color: "#4d5bd1", //仪表盘上的轴线颜色
        distance: 2, //图形与刻度的间距
      }, //刻度标签。
      axisTick: {
        show: true,
        splitNumber: 6, //刻度的段落数
        lineStyle: {
          color: "#06AEFC",
          width: 2, //刻度的宽度
          shadowColor: "#67FFFC",
          shadowBlur: 2,
        },
        length: 8, //刻度的长度
      }, //刻度样式
      pointer: {
        //表盘上的指针
        show: false,
      },
      itemStyle: {
        color: "#18c8ff",
      },

      splitLine: {
        //文字和刻度的偏移量
        show: true,
        length: 15, //便宜的长度
        lineStyle: {
          color: "#06AEFC",
          width: 2,
          shadowColor: "#67FFFC",
          shadowBlur: 1,
        },
      }, //分隔线样式
      z: 4,
    },
  ],
});
const option3 = ref({
  backgroundColor: "#161627",
  title: [
    {
      // text: '标题',
      textStyle: {
        fontSize: 18,
        color: "black",
      },
      left: "2%",
    },
    {
      text: "当前违约" + "\n" + "总人数",
      subtext: 500,
      textStyle: {
        fontSize: 19,
        color: "#FFA951",
        fontWeight: "normal",
      },
      subtextStyle: {
        fontSize: 19,
        color: "#fff",
        // fontWeight: 'bold'
      },
      textAlign: "center",
      x: "48%",
      y: "40%",
    },
  ],

  tooltip: {
    trigger: "item",
    formatter: function (parms) {
      // var str =  parms.seriesName+"</br>"+
      var str =
        parms.marker +
        "" +
        parms.data.legendname +
        "</br>" +
        "数量：" +
        parms.data.value +
        " 个</br>" +
        "占比：" +
        parms.percent +
        "%";
      return str;
    },
  },

  series: [
    {
      name: "标题",
      type: "pie",
      center: ["50%", "50%"],
      radius: ["40%", "50%"],
      clockwise: false, //饼图的扇区是否是顺时针排布
      avoidLabelOverlap: false,
      itemStyle: {
        borderColor: "#0d035c",
        borderWidth: 5,
      },
      label: {
        normal: {
          fontSize: 18,
          color: "#fff",
          formatter: function (params) {
            console.log(params, "params");
            var str = "";
            switch (params.name) {
              case "钱塘区":
                str = "{a|" + params.value + "人}\n";
                break;
              case "西湖区":
                str = "{b|" + params.value + "人}\n";
                break;
              case "余杭区":
                str = "{e|" + params.value + "人}\n";
                break;
              case "滨江区":
                str = "{d|" + params.value + "人}\n";
                break;
            }
            return str;
          },
          rich: {
            a: {
              fontSize: 18,
              color: "#03c781",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            b: {
              fontSize: 18,
              color: "#03acd1",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            c: {
              fontSize: 18,
              color: "#ff7708",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            d: {
              fontSize: 18,
              color: "#0055ff",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            e: {
              fontSize: 18,
              color: "#96b497",
              width: 38,
              height: 38,
              lineHeight: 30,
              align: "left",
            },
            nameStyle: {
              fontSize: 16,
              color: "#555",
              align: "left",
            },
            rate: {
              fontSize: 20,
              color: "#1ab4b8",
              align: "left",
            },
          },
          padding: [0, -10],
          // height: 35
        },
      },
      labelLine: {
        show: true,
        length: 20,
        length2: 35,
        smooth: false,
      },
      data: [
        {
          value: 80,
          legendname: "钱塘区",
          name: "钱塘区",
          itemStyle: { color: "#03acd1" },
        },
        {
          value: 150,
          legendname: "西湖区",
          name: "西湖区",
          itemStyle: { color: "#03c781" },
        },
        {
          value: 45,
          legendname: "余杭区",
          name: "余杭区",
          itemStyle: { color: "#96b497" },
        },
        {
          value: 150,
          legendname: "滨江区",
          name: "滨江区",
          itemStyle: { color: "#0055ff" },
        },
      ],
      z: 9,
    },
    {
      center: ["50%", "50%"], //仪表的位置
      name: "刻度", //仪表的名字
      type: "gauge", //统计图类型为仪表
      radius: 160, //统计图的半径大小
      min: 0, //最小刻度
      max: 100, //最大刻度
      splitNumber: 9, //刻度数量
      startAngle: 1, //开始刻度的角度
      endAngle: 360, //结束刻度的角度
      axisLine: {
        //设置默认刻度盘上的刻度不显示，重新定义刻度盘
        show: false,
        lineStyle: {
          width: 1,
          color: [[1, "rgba(255,255,255,0)"]],
        },
      }, //仪表盘轴线
      axisLabel: {
        //仪表盘上的数据
        show: false,
        color: "#4d5bd1", //仪表盘上的轴线颜色
        distance: 2, //图形与刻度的间距
      }, //刻度标签。
      axisTick: {
        show: true,
        splitNumber: 6, //刻度的段落数
        lineStyle: {
          color: "#00FCF7",
          width: 1, //刻度的宽度
          shadowColor: "#67FFFC",
          shadowBlur: 2,
        },
        length: 8, //刻度的长度
      }, //刻度样式
      pointer: {
        //表盘上的指针
        show: false,
      },
      itemStyle: {
        color: "#18c8ff",
      },

      splitLine: {
        //文字和刻度的偏移量
        show: true,
        length: 15, //便宜的长度
        lineStyle: {
          color: "#00FCF7",
          width: 4,
          shadowColor: "#67FFFC",
          shadowBlur: 4,
        },
      }, //分隔线样式
      z: 1,
    },
    {
      center: ["50%", "50%"], //仪表的位置
      name: "刻度", //仪表的名字
      type: "gauge", //统计图类型为仪表
      radius: 100, //统计图的半径大小
      min: 0, //最小刻度
      max: 100, //最大刻度
      splitNumber: 9, //刻度数量
      startAngle: 0, //开始刻度的角度
      endAngle: 360, //结束刻度的角度
      axisLine: {
        //设置默认刻度盘上的刻度不显示，重新定义刻度盘
        show: false,
        lineStyle: {
          width: 1,
          color: [[1, "rgba(255,255,255,0)"]],
        },
      }, //仪表盘轴线
      axisLabel: {
        //仪表盘上的数据
        show: false,
        color: "#4d5bd1", //仪表盘上的轴线颜色
        distance: 2, //图形与刻度的间距
      }, //刻度标签。
      axisTick: {
        show: true,
        splitNumber: 6, //刻度的段落数
        lineStyle: {
          color: "#06AEFC",
          width: 2, //刻度的宽度
          shadowColor: "#67FFFC",
          shadowBlur: 2,
        },
        length: 8, //刻度的长度
      }, //刻度样式
      pointer: {
        //表盘上的指针
        show: false,
      },
      itemStyle: {
        color: "#18c8ff",
      },

      splitLine: {
        //文字和刻度的偏移量
        show: true,
        length: 15, //便宜的长度
        lineStyle: {
          color: "#06AEFC",
          width: 2,
          shadowColor: "#67FFFC",
          shadowBlur: 1,
        },
      }, //分隔线样式
      z: 4,
    },
  ],
});
use([CanvasRenderer, PieChart, TitleComponent, TooltipComponent, LegendComponent]);

provide(THEME_KEY, "dark");

const option = ref({
  backgroundColor: "#060D2A",
  grid: {
    left: "1%",
    right: "1%",
    top: "10%",
    bottom: "10%",
    containLabel: true,
  },
  xAxis: {
    name: "行业",
    color: "white",
    type: "category",
    boundaryGap: 1,
    axisLine: {
      lineStyle: {
        color: "#ffffff80", //x轴的颜色
      },
    },
    axisTick: {
      show: false,
      // 隐藏x轴刻度线
      alignWithLabel: true,
    },
    axisLabel: {
      color: "#C5D6E6",
    },
    data: ["信息服务", "化工", "建筑", "运输", "食品"],
  },
  yAxis: [
    {
      type: "value",
      name: "违约人数",
      min: 0,
      splitLine: {
        lineStyle: {
          color: "#ffffff1a",
          type: "dashed",
        },
      },
      max: 10,
      axisLabel: {
        show: true,
        margin: 10,
        color: "#C5D6E6",
        formatter: "{value}",
      },
      axisTick: {
        alignWithLabel: true,
      },
    },
  ],
  series: [
    {
      data: [],
      type: "pictorialBar",
      showBackground: true,
      label: {
        show: true,
        position: "top",
        color: "#5797FF",
      },
      backgroundStyle: {
        color: "rgba(255, 255, 255, 0.03)",
      },
      barCategoryGap: "40%",
      // https://echarts.apache.org/zh/option.html#series-pictorialBar.symbol
      symbol: "triangle",
      itemStyle: {
        normal: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: "#5797FF",
            },
            {
              offset: 1,
              color: "rgba(87,151,255,0)",
            },
          ]),
        },
      },
      emphasis: {
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: "#D2FF77",
            },
            {
              offset: 1,
              color: "rgba(210,255,119,0)",
            },
          ]),
          // 鼠标滑过时柱状图的颜色
          opacity: 1, // 鼠标滑过时柱状图的透明度
        },
        label: {
          show: true,
          // 鼠标滑过时是否显示标签
          position: "top",
          // 鼠标滑过时标签位置
          textStyle: {
            color: "#D2FF77",
            // 鼠标滑过时柱状图的颜色
            opacity: 1, // 鼠标滑过时柱状图的透明度
          },
        },
      },
    },
    {
      type: "bar",
      barWidth: "60%",
      symbol: "path://M0,10 L10,10 C5.5,10 5.5,5 5,0 C4.5,5 4.5,10 0,10 z",
      itemStyle: {
        normal: {
          color: "rgba(255, 255, 255, 0.08)",
        },
      },
      data: [200, 200, 200, 200, 200, 200, 200],
      z: "-99",
    },
    // 带边框的圆圈
    {
      type: "scatter",
      symbolSize: 12,
      zlevel: 13,
      itemStyle: {
        borderWidth: 1,
        borderColor: "#5797FF",
        color: "rgba(0, 0, 0, 0)",
        opacity: 1,
      },
      silent: true,
      data: [120, 200, 150, 80, 70, 110, 130],
    },
    // 实心圆圈
    {
      type: "scatter",
      symbolSize: 6,
      zlevel: 12,
      itemStyle: {
        color: {
          type: "radial",
          r: 1,
          colorStops: [
            {
              offset: 0,
              color: "#fff",
            },
            {
              offset: 1,
              color: "#fff",
            },
          ],
          global: false,
        },
      },
      silent: true,
      data: [120, 200, 150, 80, 70, 110, 130],
    },
  ],
});
const option2 = ref({
  backgroundColor: "#060D2A",
  grid: {
    left: "1%",
    right: "1%",
    top: "10%",
    bottom: "10%",
    containLabel: true,
  },
  xAxis: {
    name: "地域",
    color: "white",
    type: "category",
    boundaryGap: 1,
    axisLine: {
      lineStyle: {
        color: "#ffffff80", //x轴的颜色
      },
    },
    axisTick: {
      show: false,
      // 隐藏x轴刻度线
      alignWithLabel: true,
    },
    axisLabel: {
      color: "#C5D6E6",
    },
    data: ["钱塘区", "西湖区", "余杭区", "滨江区"],
  },
  yAxis: [
    {
      type: "value",
      name: "违约人数",
      min: 0,
      splitLine: {
        lineStyle: {
          color: "#ffffff1a",
          type: "dashed",
        },
      },
      max: 10,
      axisLabel: {
        show: true,
        margin: 10,
        color: "#C5D6E6",
        formatter: "{value}",
      },
      axisTick: {
        alignWithLabel: true,
      },
    },
  ],
  series: [
    {
      data: [],
      type: "pictorialBar",
      showBackground: true,
      label: {
        show: true,
        position: "top",
        color: "#5797FF",
      },
      backgroundStyle: {
        color: "rgba(255, 255, 255, 0.03)",
      },
      barCategoryGap: "40%",
      // https://echarts.apache.org/zh/option.html#series-pictorialBar.symbol
      symbol: "triangle",
      itemStyle: {
        normal: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: "#5797FF",
            },
            {
              offset: 1,
              color: "rgba(87,151,255,0)",
            },
          ]),
        },
      },
      emphasis: {
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: "#D2FF77",
            },
            {
              offset: 1,
              color: "rgba(210,255,119,0)",
            },
          ]),
          // 鼠标滑过时柱状图的颜色
          opacity: 1, // 鼠标滑过时柱状图的透明度
        },
        label: {
          show: true,
          // 鼠标滑过时是否显示标签
          position: "top",
          // 鼠标滑过时标签位置
          textStyle: {
            color: "#D2FF77",
            // 鼠标滑过时柱状图的颜色
            opacity: 1, // 鼠标滑过时柱状图的透明度
          },
        },
      },
    },
    {
      type: "bar",
      barWidth: "60%",
      symbol: "path://M0,10 L10,10 C5.5,10 5.5,5 5,0 C4.5,5 4.5,10 0,10 z",
      itemStyle: {
        normal: {
          color: "rgba(255, 255, 255, 0.08)",
        },
      },
      data: [200, 200, 200, 200, 200, 200, 200],
      z: "-99",
    },
    // 带边框的圆圈
    {
      type: "scatter",
      symbolSize: 12,
      zlevel: 13,
      itemStyle: {
        borderWidth: 1,
        borderColor: "#5797FF",
        color: "rgba(0, 0, 0, 0)",
        opacity: 1,
      },
      silent: true,
      data: [120, 200, 150, 80, 70, 110, 130],
    },
    // 实心圆圈
    {
      type: "scatter",
      symbolSize: 6,
      zlevel: 12,
      itemStyle: {
        color: {
          type: "radial",
          r: 1,
          colorStops: [
            {
              offset: 0,
              color: "#fff",
            },
            {
              offset: 1,
              color: "#fff",
            },
          ],
          global: false,
        },
      },
      silent: true,
      data: [120, 200, 150, 80, 70, 110, 130],
    },
  ],
});
</script>
<style scoped>
.chart {
  height: 70vh;
  width: 70vh;
}
</style>
