if (window.yourlabs == undefined) window.yourlabs = {};

yourlabs.Table = function(table) {
    this.table = table;
    this.draggingClass = 'dragging';
    this.draggingIndex = null;
}

yourlabs.Table.prototype.initialize = function() {
    this.table.find('th')
        .prepend('<span class="handle"></span>')
        .draggable({
            cursor: 'move',
            helper: $.proxy(this.draggableHelper, this),
            start: $.proxy(this.draggableStart, this),
            stop: $.proxy(this.draggableStop, this),
            handle: '.handle',
            tolerance: 'pointer',
            opacity: 0.65,
            // snap: '.placeholder',
            // snapMode: 'inner',
            // snapTolerance: 50,
            axis: 'x',
        });

    this.resetDroppable();
}

yourlabs.Table.prototype.resetDroppable = function() {
    this.table.find('.placeholder').remove()

    var placeholder = '<td class="placeholder"></td>';

    this.table.find('th, td').before(placeholder);
    this.table.find('tr').append(placeholder)

    this.table.find('th, td:not(.placeholder)')
        .droppable({
            hoverClass: 'active',
            greedy: true,
            tolerance: 'pointer',
            over: $.proxy(this.droppableOver, this),
            out: $.proxy(this.droppableOut, this),
            drop: $.proxy(this.droppableDrop, this),
            stop: $.proxy(this.droppableStop, this),
        });
}

yourlabs.Table.prototype.draggableHelper = function(e) {
    this.draggingIndex = $(e.currentTarget).index() + 1;

    var rows = [];

    this.getColumn(this.draggingIndex).each(function() {
        rows.push('<tr>')
        rows.push($('<tr>').html($(this).clone()).html());
        rows.push('</tr>')
    })

    return $('<table class="helper">').html(rows.join(''));
}

yourlabs.Table.prototype.draggableStart = function(e, ui) {
    this.draggingIndex = $(e.currentTarget).index() + 1;
    this.getColumn(this.draggingIndex).addClass('dragging');
}

yourlabs.Table.prototype.draggableStop = function(e, ui) {
    this.table.find('.placeholder.active').removeClass('active')
    this.table.find('.dragging').removeClass('dragging');
    this.draggingIndex = null;
}

yourlabs.Table.prototype.getColumn = function(index) {
    return this.table.find('td:nth-child(' + index + '), th:nth-child(' + index + ')');
}

yourlabs.Table.prototype.droppableOver = function(e, ui) {
    this.droppableIndex = $(e.target).index() + 1;

    this.activePlaceholder = this.droppableIndex + 1;

    this.table.find('.placeholder').removeClass('active')
    this.getColumn(this.activePlaceholder).addClass('active')
}

yourlabs.Table.prototype.droppableOut = function(e, ui) {
    this.getColumn(this.activePlaceholder).removeClass('active')
}

yourlabs.Table.prototype.droppableStop = function(e, ui) {
    this.table.find('.placeholder.active').removeClass('active')
}

yourlabs.Table.prototype.droppableDrop = function(e, ui) {
    this.table.find('.placeholder.active').removeClass('active')

    var draggedColumn = this.getColumn(this.draggingIndex);
    var droppedColumn = this.getColumn(this.droppableIndex);

    for (var i=0; i<draggedColumn.length; i++) {
        $(draggedColumn.get(i)).insertAfter(droppedColumn.get(i))
    }
    
    this.resetDroppable();

    this.table.trigger('columnMoved');
}

$.fn.yourlabsTable = function(overrides) {
    if (this.length < 1) return;

    var overrides = overrides ? overrides : {};

    if (this.data('yourlabsTable') == undefined) {
        var table = new yourlabs.Table(this);
        table = $.extend(table, overrides);
        this.data('yourlabsTable', table);
        table.initialize();
    }

    return this.data('yourlabsTable');
}
