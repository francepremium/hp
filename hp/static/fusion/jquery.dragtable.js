if (window.yourlabs == undefined) window.yourlabs = {};

yourlabs.Table = function(table) {
    // <table> element.
    this.table = table;

    // Index of the column being drag.
    this.dragIndex = null;

    // Index of the column being hovered or drop on.
    this.dropIndex = null;

    // Drag column handle which will be prepended to th.
    this.dragHandleHtml = '<span class="handle drag-handle"></span>';

    // Selector string for dragHandleHtml.
    this.dragHandleSelector = '.drag-handle';

    // CSS class for the column being drag. Will be set on all td, ths.
    this.dragColumnClass = 'dragging';

    // Selector string for the column being drag.
    this.dragColumnSelector = '.' + this.dragColumnClass;

    // HTML used to create the semi transparent drag helper. It will be filled
    // with copies of the contents of the column being drag.
    this.helperTableHtml = '<table class="helper">';

    // Cell HTML used to create placeholder columns.
    this.placeholderHtml = '<td class="placeholder"></td>';

    // Selector string for placeholderHtml
    this.placeholderSelector = '.placeholder';

    // CSS class that should be added to placeholder when they become active.
    this.placeholderActiveClass = 'active';

    // Selector string for active placeholders
    this.placeholderActiveSelector = [
        this.placeholderSelector,
        '.',
        this.placeholderActiveClass
    ].join('')
}

yourlabs.Table.prototype.initialize = function() {
    this.table.find('th')
        .prepend(this.dragHandleHtml)
        .draggable({
            cursor: 'move',
            helper: $.proxy(this.dragHelper, this),
            start: $.proxy(this.dragStart, this),
            stop: $.proxy(this.stopDrag, this),
            handle: this.dragHandleSelector,
            tolerance: 'pointer',
            opacity: 0.65,
            axis: 'x',
        });

    
    this.table.find('th, td')
        .droppable({
            greedy: true,
            tolerance: 'pointer',
            over: $.proxy(this.dropOver, this),
            drop: $.proxy(this.stopDrag, this),
        });
    
    this.createPlaceholders();
}

// Remove all placeholder cells.
yourlabs.Table.prototype.removePlaceholders = function() {
    this.table.find(this.placeholderSelector).remove()
}

// Create a placeholder column after each actual column.
yourlabs.Table.prototype.createPlaceholders = function() {
    this.table.find('th, td').before(this.placeholderHtml);
    this.table.find('tr').append(this.placeholderHtml)
}

yourlabs.Table.prototype.dragHelper = function(e) {
    this.dragIndex = $(e.currentTarget).index() + 1;

    var rows = [];

    this.getColumn(this.dragIndex).each(function() {
        rows.push('<tr>')
        rows.push($('<tr>').html($(this).clone()).html());
        rows.push('</tr>')
    })

    return $(this.helperTableHtml).html(rows.join(''));
}

// On drag start, note the dragged column index and set dragColumnClass.
yourlabs.Table.prototype.dragStart = function(e, ui) {
    this.dragIndex = $(e.currentTarget).index() + 1;
    this.getColumn(this.dragIndex).addClass(this.dragColumnClass);
}

// On drag stop, get the drop column index, move the cells, trigger columnMoved
// and clean up.
yourlabs.Table.prototype.stopDrag = function(e, ui) {
    if (this.dragIndex == null) {
        // stopDrag was already called.
        return;
    }

    this.dropIndex = this.table.find(
        this.placeholderActiveSelector + ':first').index();

    this.table.find(this.placeholderActiveSelector)
        .removeClass(this.placeholderActiveClass)

    this.table.find(this.dragColumnSelector)
        .removeClass(this.dragColumnClass);

    var dragColumn = this.getColumn(this.dragIndex);
    var dropColumn = this.getColumn(this.dropIndex);

    for (var i=0; i<dragColumn.length; i++) {
        $(dragColumn.get(i)).insertAfter(dropColumn.get(i))
    }

    this.dragIndex = null;
    this.dropIndex = null;

    this.removePlaceholders();
    // Trigger columnMoved while the table is clean from fake columns.
    this.table.trigger('columnMoved');
    this.createPlaceholders();
}

// Return all cells of a particular column.
yourlabs.Table.prototype.getColumn = function(index) {
    return this.table.find(
        'td:nth-child(' + index + '), th:nth-child(' + index + ')');
}

// On drop over, update active placeholder.
yourlabs.Table.prototype.dropOver = function(e, ui) {
    this.dropIndex = $(e.target).index() + 1;

    this.activePlaceholder = this.dropIndex + 1;

    this.table.find(this.placeholderSelector)
        .removeClass(this.placeholderActiveClass)
    this.getColumn(this.activePlaceholder)
        .addClass(this.placeholderActiveClass)
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
