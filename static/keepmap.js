var mapObj;
function sleep(numberMillis) { 
    var now = new Date(); 
    var exitTime = now.getTime() + numberMillis; 
    while (true) { 
    now = new Date(); 
    if (now.getTime() > exitTime) 
    return; 
    } 
}

var lnglatList;
function showHeatMap(){
    mapObj.destroy()
    if(lnglatList){
        loadHeatMap(lnglatList)

    }else{

        alert('请等待数据加载完毕')
    }

}
function showPointMap(){

    mapObj.destroy()
    if(lnglatList){

        loadMuchPoints(lnglatList)
    }else{

        alert('请等待数据加载完毕')
    }

}


function loadtsvHeatMap(lnglatData){
    var map = Loca.create('container', {
        mapStyle: 'amap://styles/twilight',
        zoom: 9,
        pitch: 50,
        center: [120.198254, 36.465551],
        zooms: [4, 11]
    });
    var layer = Loca.visualLayer({
        eventSupport: true, // 触发 selectStyle 需要开始事件拾取
        container: map,
        type: 'heatmap',
        shape: 'rectangle'
    });

    layer.setData(lnglatData, {
        lnglat: function (obj) {
            print(obj)
            return [obj.lnglat[0], obj.lnglat[1]]
        },
        value: 'count',
        type: 'tsv'
    });

    layer.setOptions({
        unit: 'meter',
        style: {
            color: ['#ecda9a', '#efc47e', '#f3ad6a', '#f7945d', '#f97b57', '#f66356', '#ee4d5a'],
            radius: 3000,
            opacity: 0.85,
            height: [100, 500000],
            gap: 300
        },
        selectStyle: {
            color: '#fcff19'
        }
    });

    layer.render();

}

function loadHeatMap(lnglatData){
    var map = Loca.create('container', {
        features: ['bg', 'road'],
        center: [116.397475, 39.908668],
        pitch: 50,
        zoom: 10,
        // Loca 自 1.2.0 起 viewMode 模式默认为 3D，如需 2D 模式，请显示配置。
        viewMode: '2D'
    });
    var layer = Loca.visualLayer({
        container: map,
        type: 'heatmap',
        // 基本热力图
        shape: 'normal'
    });

    var list = [];
    var i = -1, length = lnglatData.length;
    while (++i < length) {
        var item = lnglatData[i];
        if(i==10){

            print(item)
        }
        list.push({
            coordinate: [item.lnglat[0], item.lnglat[1]],

        })
    }

    layer.setData(list, {
        lnglat: 'coordinate',
        value: 'count'
    });

    layer.setOptions({
        style: {
            radius: 30,
            color: {
                0.5: '#2c7bb6',
                0.65: '#abd9e9',
                0.7: '#ffffbf',
                0.9: '#fde468',
                1.0: '#d7191c'
            }
        }
    });

    layer.render();

}
function onMapLoadComplete(res){

     print(res)
     getKeepTrain()
    // loadHeatMap()
}
function onMapRightClick(res){

    latlng = res['lnglat']
    lat = latlng['O']
    lng = latlng['P']
    print(lng+","+lat)
    print(res)
    var url = 'http://127.0.0.1:5000/nearbyuser?lat='+lat+"&lng="+lng
    print(url)
    $.ajax(url,{
        method:"GET",
        headers:{
            'Access-Control-Allow-Origin':'*',
        },
        jsonp:"jsonpCallback",
        jsonpCallback:"success_jsonpCallback",
        dataType:'jsonp',
        success:function(data){

            print(data)
        }

    })
    // const body = {name:"Good boy"};

    // fetch(url,{
    //     mode: 'no-cors',
    //     method:"GET",
    //     headers:{
    //         'Access-Control-Allow-Origin':'*',
    //         'Accept': 'application/json, text/plain, */*',
    //         'Content-Type': 'application/x-www-form-urlencoded'
    //     },
    //     credentials: 'include',
    // }).then(function(data){
    //     print(data)
    // })

}
function parseJSON(response) {
    return response.json
  }
function print(obj){
    console.log(obj)
}
function printE(err){
    console.error(err)
}
var userList = new Array()
function success_jsonpCallback(result){

    // console.log(result)
}
function getKeepTrain(){

    $.ajax({

        //callback=jQuery2140990458214547516_1543977083173&_=1543977083174
        url:'http://arestory.info:9090/trains/geo/1/30000',
        dataType:'jsonp',
        jsonp:"jsonpCallback",
        jsonpCallback:"success_jsonpCallback",
        headers:{
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Headers':'x-requested-with,content-type'
        },
        error:function(){

            console.log('wrong')
        },
        success:function(data){

            // console.log(data)
            var lnglatData = new Array()
            var index = 0
            for(var i =0;i<data.length;i++){
                var train =  data[i]

                var lat = train['latitude']
                var lng = train['longitude']
                var iconUrl = train['photo']
                lnglatData[index] = {
                    'lnglat':[parseFloat(lng),parseFloat(lat)],
                    id :index
                }
                // addMarker(lat,lng,iconUrl)
                // addTrainSimpleMarker(lat,lng)
                if(!(train['author_id'] in userList)){

                    userList[index] = train['author_id']
                    //
                    index = index+1
                    // sleep(2000*(index))
                    var funname = "getUserInfo("+"'"+train['author_id']+"',"+lat+","+lng+")"
                    //  setTimeout(funname,300*index)
                }
            }
            lnglatList = lnglatData
             console.log(data)
            loadMuchPoints(data)
            // loadHeatMap(lnglatData)
            // loadtsvHeatMap(lnglatData)
        }



    })

}

function getUserInfo2(lat,lng,userId){

    user_url = 'http://127.0.0.1:5000/userinfo/'+userId
    $.ajax({

        url:user_url,
        dataType:'jsonp',
        jsonp:"jsonpCallback",
        jsonpCallback:"success_jsonpCallback",
        headers:{
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Headers':'x-requested-with,content-type'
        },
        error:function(){

            console.log('wrong')
        },
        success:function(data){
              console.log(data)
              var user = eval(data)
            iconUrl = user['avatar']
            console.log(user['name'])
            showUserWindow2(lat,lng,user)
        }

    })

}

function getUserInfo(userId,lat,lng){

    user_url = 'http://127.0.0.1:5000/userinfo/'+userId
    $.ajax({

        url:user_url,
        dataType:'jsonp',
        jsonp:"jsonpCallback",
        jsonpCallback:"success_jsonpCallback",
        headers:{
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Headers':'x-requested-with,content-type'
        },
        error:function(){

            console.log('wrong')
        },
        success:function(data){
              console.log(data)
              var user = eval(data)
            iconUrl = user['avatar']
            console.log(user['name'])
            addUserSimpleMarker(lat,lng,user)
        }

    })

}

function onMapLoadError(){


}
function showTrainWindow(train){
    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function(SimpleInfoWindow) {

        var author_name = train['author_name']

        var position = [parseFloat(train['longitude']),parseFloat(train['latitude'])]
        var arr =  train['photo'].split('_')
        var width=300
        var height =300
        if(arr.length>1){
            var bili =arr[1]
            bili = bili.split('.')[0]
            bili = bili.split('x')
             width = parseInt(bili[0])
             height = parseInt(bili[1])
            bili = parseInt(bili[0])/parseInt(bili[1])
            console.log("图片比例："+width+":"+height)
            if(width>300){
                width=300
            }
            height = parseInt(width/bili)
            console.log("转换图片比例："+width+":"+height)
        }


        var id = train['author_id']

        var lat = parseFloat(train['latitude'])
        var lng = parseFloat(train['longitude'])
        var clickFun = "getUserInfo2('"+lat+"','"+lng+"','"+id+"')"
        var infoWindow = new SimpleInfoWindow({
            infoTitle: '<button onclick="'+clickFun+'">'+author_name+'</button>',
            infoBody: '<p style="width:'+width+'px;" class="my-desc"><img style="height:'+height+'px;width:'+width+'px" src ="'+train['photo']+'"></img><br/><strong>'+train['created']+'</strong><br/>'+train['content']+'<br/></p>',

            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });
        infoWindow.open(mapObj,position)

    })

}
function showUserWindow2(lat,lng,user){
    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function(SimpleInfoWindow) {

        var sex = "男"
        if(user['gender']=="F"){
            sex = "女"
        }
        var arr =  user['avatar'].split('_')
        var width=300
        var height =300
        if(arr.length>1){
            var bili =arr[1]
            bili = bili.split('.')[0]
            bili = bili.split('x')
             width = parseInt(bili[0])
             height = parseInt(bili[1])
            bili = parseInt(bili[0])/parseInt(bili[1])
            console.log("图片比例："+width+":"+height)
            if(width>300){
                width=300
            }
            height = parseInt(width/bili)
            console.log("转换图片比例："+width+":"+height)
        }
        var birthday = user['birthday'].split('T')[0]
        var infoWindow = new SimpleInfoWindow({

            infoTitle: '<strong>'+user['name']+'</strong>',
            infoBody: '<p style="width:'+width+'px" class="my-desc"><br/><img style="height:'+height+'px;width:'+width+'px" src ="'+user['avatar']+'"></img><br/><strong>'+sex+'</strong> ,'+birthday+'<br/>'+user['bio']+'</p>',

            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });

        infoWindow.open(mapObj,[parseFloat(lng),parseFloat(lat)])

    })
}
function showUserWindow(marker,user){
    AMapUI.loadUI(['overlay/SimpleInfoWindow'], function(SimpleInfoWindow) {

        var sex = "男"
        if(user['gender']=="F"){
            sex = "女"
        }
        var infoWindow = new SimpleInfoWindow({

            infoTitle: '<strong>'+user['name']+'</strong>',
            infoBody: '<p class="my-desc"><br/><img style="height:200px;width:200px" src ="'+user['avatar']+'"></img><br/><strong>'+sex+'</strong> ,'+user['birthday']+'<br/>'+user['bio']+'</p>',

            //基点指向marker的头部位置
            offset: new AMap.Pixel(0, -31)
        });
        infoWindow.open(mapObj,marker.getPosition())

    })
}
function addTrainSimpleMarker(latitude,longitude){
    var markerElement = document.createElement('div')
    markerElement.className = "FCircle"
    // markerElement.src = user['avatar']
    // markerElement.style = "height:30px;width:30px"
    var marker=new AMap.Marker({
        topWhenClick:true,
        clickable:true,
        position:new AMap.LngLat(longitude,latitude) ,
        content :markerElement
        });
    marker.setMap(mapObj);  //在地图上添加点
//    AMap.event.addListener(marker,'click',function(){

//     showUserWindow(marker,user)
//    })
}

function addUserSimpleMarker(latitude,longitude,user){
    var markerElement = document.createElement('div')
    if(user['gender']=="F"){
        markerElement.className = "FCircle"
    }else{
        markerElement.className = "Circle"

    }
    // markerElement.src = user['avatar']
    // markerElement.style = "height:30px;width:30px"
    var marker=new AMap.Marker({
        topWhenClick:true,
        title:user['name'],
        clickable:true,
        position:new AMap.LngLat(longitude,latitude) ,
        content :markerElement
        });
    marker.setMap(mapObj);  //在地图上添加点
   AMap.event.addListener(marker,'click',function(){

    showUserWindow(marker,user)
   })
}

function addUserMarker(latitude,longitude,user){
    var markerElement = document.createElement('img')
    markerElement.src = user['avatar']
    markerElement.style = "height:30px;width:30px"
    var marker=new AMap.Marker({
        topWhenClick:true,
        icon:user['avatar'],
        title:user['name'],
        clickable:true,
        position:new AMap.LngLat(longitude,latitude) ,
        content :markerElement
        });
    marker.setMap(mapObj);  //在地图上添加点
   AMap.event.addListener(marker,'click',function(){

    showUserWindow(marker,user)
   })
}
function addMarker(latitude,longitude,iconUrl){

    var markerElement = document.createElement('img')
    markerElement.src = iconUrl
    markerElement.style = "height:30px;width:30px"
    var marker=new AMap.Marker({
        icon:iconUrl,
        position:new AMap.LngLat(longitude,latitude) ,
        content :markerElement
        });
        marker.setMap(mapObj);  //在地图上添加点
}


function initMap(){

    //创建地图
    var map = new AMap.Map('container',{
        center:[114.628467,22.861748],
        zoom:1

    });
    mapObj = map;
   //定位
   AMap.plugin('AMap.Geolocation',function(){
           geolocation = new AMap.Geolocation({
                   enableHighAccuracy: true,//是否使用高精度定位，默认:true
                   timeout: 10000,          //超过10秒后停止定位，默认：无穷大
                   maximumAge: 0,           //定位结果缓存0毫秒，默认：0
                   convert: true,           //自动偏移坐标，偏移后的坐标为高德坐标，默认：true
                   showButton: true,        //显示定位按钮，默认：true
                   buttonPosition: 'LB',    //定位按钮停靠位置，默认：'LB'，左下角
                   buttonOffset: new AMap.Pixel(10, 20),//定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
                   showMarker: true,        //定位成功后在定位到的位置显示点标记，默认：true
                   showCircle: true,        //定位成功后用圆圈表示定位精度范围，默认：true
                   panToLocation: true,     //定位成功后将定位到的位置作为地图中心点，默认：true
                   zoomToAccuracy:true      //定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
               });
           map.addControl(geolocation);
           geolocation.getCurrentPosition();
           AMap.event.addListener(geolocation, 'complete', onMapLoadComplete);//返回定位信息
           AMap.event.addListener(geolocation, 'error', onMapLoadError);      //返回定位出错信息

   })
   map.on('rightclick',onMapRightClick)
}


function loadMuchPoints(pointData){

    AMapUI.load(['ui/misc/PointSimplifier', 'lib/$', 'lib/utils'], function(PointSimplifier, $, utils) {

        if (!PointSimplifier.supportCanvas) {
            alert('当前环境不支持 Canvas！');
            return;
        }

        var defaultRenderOptions = {
            drawQuadTree: false,
            drawPositionPoint: false,
            drawShadowPoint: false,
            //点
            pointStyle: {
                content: 'circle',
                width: 10,
                height: 10,
                fillStyle: '#303F9F',
                lineWidth: 1,
                strokeStyle: 'rgba(0,0,0,0)'
            },
            //TopN区域
            topNAreaStyle: {
                autoGlobalAlphaAlpha: true,
                content: 'rect',
                fillStyle: '#e25c5d',
                lineWidth: 1,
                strokeStyle: 'rgba(0,0,0,0)'
            },
            //点的硬核部分
            pointHardcoreStyle: {
                content: 'none',
                width: 5,
                height: 5,
                lineWidth: 1,
                fillStyle: 'rgba(0,0,0,0)',
                strokeStyle: 'rgba(0,0,0,0)'
            },
            //定位点
            pointPositionStyle: {
                content: 'circle',
                width: 2,
                height: 2,
                lineWidth: 1,
                //offset: ['-50%', '-50%'],
                strokeStyle: 'rgba(0,0,0,0)',
                fillStyle: '#cc0000'
            },
            //鼠标hover时的覆盖点
            pointHoverStyle: {
                width: 10,
                height: 10,
                content: 'circle',
                fillStyle: 'rgba(0,0,0,0)',
                lineWidth: 2,
                strokeStyle: '#ffa500'
            },
            //空间被占用的点
            shadowPointStyle: {
                fillStyle: 'rgba(0,0,0,0.2)',
                content: 'circle',
                width: 6,
                height: 6,
                lineWidth: 1,
                strokeStyle: 'rgba(0,0,0,0)'
            }
        };
        var pointSimplifierIns = new PointSimplifier({

            zIndex: 100,

            map: mapObj,

            getPosition: function(item) {

                if (!item) {
                    return null;
                }

                //   var parts = item.split(',');
                //  console.log(parts)
                //lnglat
                return [item.lnglat[0],item.lnglat[1]]
                //  return [parseFloat(item['longitude']), parseFloat(item['latitude'])];]
                //  return [parseFloat(item['longitude']), parseFloat(item['latitude'])];
                // return [parseFloat(parts[0]), parseFloat(parts[1])];

            },
            compareDataItem: function(a, b, aIndex, bIndex) {

                //数据源尾部的优先
                return aIndex > bIndex ? -1 : 1;
            },
            getHoverTitle: function(dataItem, idx) {
                return idx + ': ' + dataItem;
            },
            renderOptions: defaultRenderOptions
        });

        window.pointSimplifierIns = pointSimplifierIns;

        $('<div id="loadingTip">加载数据，请稍候...</div>').appendTo(document.body);
        
        pointSimplifierIns.setData(pointData); 
        $('#loadingTip').remove();
        pointSimplifierIns.on('pointClick',function(e,record){


            showTrainWindow(record['data'])
            console.log(record['data'])
        })
        var customContainer = document.getElementById('my-gui-container');

        function createRenderEngGui() {

            function RenderEngOptions() {
                this.drawQuadTree = false;
                this.drawPositionPoint = false;
                this.drawShadowPoint = false;
                this.disableHardcoreWhenPointsNumBelow = 0;
            }

            var renderEngParams = new RenderEngOptions();

            var renderEngGui = new dat.GUI({
                width: 260,
                autoPlace: false,
            });

            renderEngGui.add(renderEngParams, 'drawQuadTree').onChange(render);

            renderEngGui.add(renderEngParams, 'drawShadowPoint').onChange(render);

            renderEngGui.add(renderEngParams, 'drawPositionPoint').onChange(render);

            //renderEngGui.add(renderEngParams, 'disableHardcoreWhenPointsNumBelow', 0, 10000).step(1000).onChange(render);

            addGuiPanel('', '', renderEngGui);

            return renderEngParams;
        }

        var customContentMap = {
            'custom_path': function setCustom1Content(params) {

                return utils.extend(params, {
                    content: function(ctx, x, y, width, height) {

                        //注意，这里的width和height可能不同于pointStyle里面的width/height， 高清屏幕下会存在比例缩放

                        //这里绘制一个菱形路径
                        var yPos = 1 / 3;

                        var top = [x + width / 2, y],
                            right = [x + width, y + height * yPos],
                            bottom = [x + width / 2, y + height],
                            left = [x, y + height * yPos];

                        ctx.moveTo(top[0], top[1]);
                        ctx.lineTo(right[0], right[1]);
                        ctx.lineTo(bottom[0], bottom[1]);
                        ctx.lineTo(left[0], left[1]);
                        ctx.lineTo(top[0], top[1]);

                    },
                    //定位点为底部中心
                    offset: ['-50%', '-100%']
                });
            },
            'custom_icon': function setCustom3Content(params) {

                return utils.extend(params, {
                    //使用图片
                    content: PointSimplifier.Render.Canvas.getImageContent(
                        'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
                        function onload() {
                            pointSimplifierIns.renderLater();
                        },
                        function onerror(e) {
                            alert('图片加载失败！');
                        }),
                    //定位点为底部中心
                    offset: ['-50%', '-100%']
                });
            }
        };

        function createPointStyleGui(target) {

            var pointStyleGui = new dat.GUI({
                width: 260,
                autoPlace: false,
            });

            var pointStyleParams = utils.extend({}, defaultRenderOptions[target]);

            //pointStyleGui.add(pointStyleParams, 'optionName');

            //形状类型
            pointStyleGui.add(pointStyleParams, 'content', ['rect', 'circle', 'none', 'custom_path', 'custom_icon']).onChange(render);

            if (target !== 'topNAreaStyle') {

                //宽度
                pointStyleGui.add(pointStyleParams, 'width', 0, 50).step(1).onChange(render);

                //高度
                pointStyleGui.add(pointStyleParams, 'height', 0, 50).step(1).onChange(render);

            } else {
                pointStyleGui.add(pointStyleParams, 'autoGlobalAlphaAlpha').onChange(render);
            }

            pointStyleGui.addColor(pointStyleParams, 'fillStyle').onChange(render);

            pointStyleGui.addColor(pointStyleParams, 'strokeStyle').onChange(render);

            pointStyleGui.add(pointStyleParams, 'lineWidth', 1, 10).step(1).onChange(render);

            addGuiPanel(target, target, pointStyleGui);

            return pointStyleParams;
        }

        function addGuiPanel(id, title, gui) {

            var container = document.createElement('div');

            container.id = id;

            if (title) {
                var tEle = document.createElement('h3');
                tEle.innerHTML = title;
                container.appendChild(tEle);
            }

            container.appendChild(gui.domElement);

            customContainer.appendChild(container);
        }

        var styleOptions = ['pointStyle', 'topNAreaStyle', 'pointHardcoreStyle', 'pointPositionStyle', 'pointHoverStyle', 'shadowPointStyle'];

        var renderEngParams = createRenderEngGui(),
            styleParamsMap = {};

        for (var i = 0, len = styleOptions.length; i < len; i++) {
            styleParamsMap[styleOptions[i]] = createPointStyleGui(styleOptions[i]);
        }

        function render() {

            $('#shadowPointStyle').toggleClass('hide', !renderEngParams.drawShadowPoint);

            $('#pointPositionStyle').toggleClass('hide', !renderEngParams.drawPositionPoint);

            pointSimplifierIns.renderEngine.setOptions(renderEngParams);

            for (var k in styleParamsMap) {

                var params = utils.extend({}, styleParamsMap[k]);

                if (customContentMap[params['content']]) {
                    params = customContentMap[params['content']](params);
                }

                pointSimplifierIns.renderEngine.setOption(k, params);
            }

            pointSimplifierIns.renderLater(200);

            refreshConfigPanel();
        }

        var colorFlds = ['fillStyle', 'strokeStyle', 'borderStyle'],
            rgbAlphaRegx = /([\d\.]+)\s*\)/i;

        function isEmptyColor(color) {

            if (color.indexOf('rgba') !== 0) {
                return false;
            }

            var match = color.match(rgbAlphaRegx);

            if (match && parseFloat(match[1]) < 0.01) {
                return true;
            }

            return false;
        }

        function fixColors(opts) {

            if (utils.isObject(opts)) {

                for (var i = 0, len = colorFlds.length; i < len; i++) {

                    if (opts[colorFlds[i]] && isEmptyColor(opts[colorFlds[i]])) {
                        opts[colorFlds[i]] = null;
                    }
                }
            }

            return opts;
        }


        function exportRenderOptions() {

            var options = utils.extend({}, renderEngParams);

            for (var k in defaultRenderOptions) {

                var opts = styleParamsMap[k];

                if (opts) {
                    options[k] = fixColors(opts);
                }
            }
            return options;
        }

        function refreshConfigPanel() {

            var options = exportRenderOptions();

            var configStr = 'renderOptions: ' + JSON.stringify(options, null, 2);

            $('#exportConfigPanel').find('pre').html(configStr);
        }

        $('#exportBtn').click(function() {

            var panel = $('#exportConfigPanel');

            if (!panel.length) {
                panel = $('<div id="exportConfigPanel"><pre></pre></div>').appendTo(document.body);
                $(this).html('隐藏配置信息');

            } else {
                $(this).html('显示配置信息');
                panel.remove();
                return;
            }
            refreshConfigPanel();
        });

        render();
    });

}