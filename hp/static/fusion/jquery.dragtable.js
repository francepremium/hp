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
            snapTolerance: 50,
            snapMode: 'inner',
        });

    this.resetDroppable();
}

yourlabs.Table.prototype.resetDroppable = function() {
    this.table.find('.placeholder').droppable('destroy').remove();

    var placeholder = '<td class="placeholder"></td>';

    this.table.find('th, td').before(placeholder);
    this.table.find('tr').append(placeholder)

    this.table.find('.placeholder')
        .droppable({
            hoverClass: 'active',
            greedy: true,
            over: $.proxy(this.droppableOver, this),
            out: $.proxy(this.droppableOut, this),
            drop: $.proxy(this.droppableDrop, this),
        });
    
    this.table.find('th')
        .droppable('option', 'snap', '.placeholder')
}

yourlabs.Table.prototype.draggableHelper = function(e) {
    this.draggingIndex = $(e.currentTarget).index() + 1;

    var rows = [];

    this.draggedTds().each(function() {
        rows.push('<tr>')
        rows.push($('<tr>').html($(this).clone()).html());
        rows.push('</tr>')
    })

    return $('<table class="helper">').html(rows.join(''));
}

yourlabs.Table.prototype.draggableStart = function(e, ui) {
    this.draggingIndex = $(e.currentTarget).index() + 1;
    this.draggedTds().addClass('dragging');

    this.table.find('.placeholder')
        .not(':nth-child(' + (this.draggingIndex+1 ) + ')')
        .not(':nth-child(' + (this.draggingIndex-1 ) + ')')
        .addClass('usable');


    this.table.find('.placeholder.usable').droppable({disabled: false});
    this.table.find('.placeholder:not(.usable)').droppable({disabled: true});
}

yourlabs.Table.prototype.draggableStop = function(e, ui) {
    this.table.find('.dragging').removeClass('dragging');
    this.table.find('.usable').removeClass('usable');
    this.draggingIndex = null;
}

yourlabs.Table.prototype.draggedTds = function() {
    if (!this.draggingIndex) return;
    return this.table.find('td:nth-child(' + this.draggingIndex + '), th:nth-child(' + this.draggingIndex + ')');
}

yourlabs.Table.prototype.droppableTds = function() {
    if (!this.droppableIndex) return;
    return this.table.find('td:nth-child(' + this.droppableIndex + '), th:nth-child(' + this.droppableIndex + ')');
}

yourlabs.Table.prototype.droppableOver = function(e, ui) {
    this.droppableIndex = $(e.target).index() + 1;
    this.droppableTds().addClass('active');
}

yourlabs.Table.prototype.droppableOut = function(e, ui) {
    this.table.find('.placeholder.usable.active').removeClass('active');
}

yourlabs.Table.prototype.droppableDrop = function(e, ui) {
    for (var i=0; i<this.draggedTds().length; i++) {
        $(this.draggedTds().get(i)).insertAfter(this.droppableTds().get(i))
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
