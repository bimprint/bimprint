"use strict"

/**
 * Class: BIMSURFER.Control.ClickSelect
 * Control to select and hightlight a Scene JS by clicking on it.
 */
BIMSURFER.Control.ClickSelect = BIMSURFER.Class(BIMSURFER.Control, {
	CLASS: "BIMSURFER.Control.ClickSelect",

	/**
	 * X coordinate of the last mouse event
	 */
	downX: null,

	/**
	 * Y coordinate of the last mouse event
	 */
	downY: null,
	
	active: false,

	/**
	 * The selected and highlighted SceneJS node
	 */
	highlighted: null,

	/**
	 * Timestamp of the last selection
	 */
	lastSelected: 0,

	/**
	 * Constructor.
	 *
	 * @constructor
	 */
	__construct: function() {
		this.events = new BIMSURFER.Events(this);
	},

	/**
	 * Activates the contol
	 */
	activate: function() {
		if(this.SYSTEM == null || !this.SYSTEM.sceneLoaded) {
			console.error('Cannot activate ' + this.CLASS + ': Surfer or scene not ready');
			return null;
		}
		if (!this.active) {
			this.active = true;
			this.initEvents();
			this.events.trigger('activated');
		}
		return this;
	},

	/**
	 * Initializes the events necessary for the operation of this control
	 *
	 * @return this
	 */
	initEvents: function() {
		if(this.active) {
			this.SYSTEM.events.register('pick', this.pick, this);
			this.SYSTEM.events.register('mouseDown', this.mouseDown, this);
			this.SYSTEM.events.register('mouseUp', this.mouseUp, this);
		} else {
			this.SYSTEM.events.unregister('pick', this.pick, this);
			this.SYSTEM.events.unregister('mouseDown', this.mouseDown, this);
			this.SYSTEM.events.unregister('mouseUp', this.mouseUp, this);
		}
		return this;
	},

	/**
	 * Event listener
	 *
	 * @param {mouseEvent} e Mouse event
	 */
	mouseDown: function(e) {
		this.downX = e.offsetX;
		this.downY = e.offsetY;
	},

	/**
	 * Event listener
	 *
	 * @param {mouseEvent} e Mouse event
	 */
	mouseUp: function(e) {
		if(((e.offsetX > this.downX) ? (e.offsetX - this.downX < 5) : (this.downX - e.offsetX < 5)) &&	((e.offsetY > this.downY) ? (e.offsetY - this.downY < 5) : (this.downY - e.offsetY < 5))) {
			if(Date.now() - this.lastSelected > 10) {
				this.unselect();
			}
		}
	},

	/**
	 * Event listener
	 *
	 * @param {SceneJS.node} hit Selected SceneJS node
	 */
	pick: function(hit) {
		this.unselect();
		this.highlighted = this.SYSTEM.scene.findNode(hit.nodeId);
		var groupId = this.highlighted.findParentByType("translate").data.groupId;

		var matrix = this.highlighted.nodes[0];
		var geometryNode = matrix.nodes[0];

		if (geometryNode._core.arrays.colors != null) {
			var geometry = {
				type: "geometry",
				primitive: "triangles"
			};
	
			geometry.coreId = geometryNode.getCoreId() + "Highlighted";
			geometry.indices = geometryNode._core.arrays.indices;
			geometry.positions = geometryNode._core.arrays.positions;
			geometry.normals = geometryNode._core.arrays.normals;
			
			geometry.colors = [];
			for (var i=0; i<geometryNode._core.arrays.colors.length; i+=4) {
				geometry.colors[i] = 0;
				geometry.colors[i+1] = 1;
				geometry.colors[i+2] = 0;
				geometry.colors[i+3] = 1;
			}
			
			var library = this.SYSTEM.scene.findNode("library-" + groupId);
			library.add("node", geometry);
			
			var newGeometry = {
				type: "geometry",
				coreId: geometryNode.getCoreId() + "Highlighted"
			}
			
			matrix.removeNode(geometryNode);
			matrix.addNode(newGeometry);
		}
		
		this.highlighted.insert('node', BIMSURFER.Constants.highlightSelectedObject);
		this.lastSelected = Date.now();
		var o = this;
		window.setTimeout(function(){
			o.events.trigger('select', [groupId, o.highlighted]);
		}, 0);
	},

	/**
	 * Event listener
	 */
	unselect: function() {
		var highlighted = this.SYSTEM.scene.findNode(BIMSURFER.Constants.highlightSelectedObject.id);
		if (highlighted != null) {
			var groupId = highlighted.findParentByType("translate").data.groupId;
			if(highlighted != null)
			{
				var matrix = highlighted.nodes[0];
				var geometryNode = matrix.nodes[0];
				
				if (geometryNode._core.arrays.colors != null) {
					matrix.removeNode(geometryNode);
					
					var newGeometry = {
						type: "geometry",
						coreId: geometryNode.getCoreId().replace("Highlighted", "")
					}
					
					matrix.addNode(newGeometry);
				}
				
				highlighted.splice();
				
				this.events.trigger('unselect', [this.highlighted == null ? null : this.highlighted.findParentByType("translate").groupId, this.highlighted]);
				this.highlighted = null;
			}
		}
	}
});