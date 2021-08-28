<template>
    <div class="background">
        <div class="m-5">
            <b-table
                :data="currentOperation"
                :loading="loading"
                :per-page="perPage"
                paginated
                backend-pagination
                :total="paginationCount"
                @page-change="onPageChange"
                backend-sorting
                :default-sort-direction="defaultSortOrder"
                :default-sort="[sortField, sortOrder]"
                @sort="onSort"
                backend-filtering
                @filters-change="onFiltersChange"
                :debounce-search="1000"
                :sticky-header="true"
                :height="840"
                hoverable
                ref="table"
                detailed
                detail-key="id"
            >
                <template>
                    <b-table-column
                        field="id"
                        label="ID"
                        numeric
                        sortable
                        v-slot="props"
                        width="40"
                    >
                        {{ props.row.id }}
                    </b-table-column>
                    <b-table-column
                        field="date"
                        label="Date"
                        sortable
                        searchable
                        centered
                    >
                        <template #searchable="props">
                            <b-field>
                                <b-datepicker
                                    v-model="props.filters[props.column.field]"
                                    placeholder="Select date..."
                                    icon="calendar-today"
                                    trap-focus
                                >
                                    <b-button
                                        label="Clear"
                                        type="is-danger"
                                        icon-left="close"
                                        outlined
                                        @click="
                                            props.filters[props.column.field] = null
                                        "
                                    />
                                </b-datepicker>
                            </b-field>
                        </template>
                        <template v-slot="props">
                            {{ new Date(props.row.date).toLocaleDateString() }}
                        </template>
                    </b-table-column>
                    <b-table-column
                        field="time"
                        label="Time"
                        v-slot="props"
                        sortable
                        centered
                    >
                        {{ props.row.time }}
                    </b-table-column>
                    <b-table-column
                        field="category"
                        label="Category"
                        sortable
                        searchable
                        centered
                    >
                        <template #searchable="props">
                            <b-field>
                                <b-select
                                    v-model="props.filters[props.column.field]"
                                    placeholder="Categories"
                                >
                                    <option :value="null"></option>
                                    <option value="Housing">Housing</option>
                                    <option value="Eating out">Eating out</option>
                                    <option value="Groceries">Groceries</option>
                                </b-select>
                            </b-field>
                        </template>
                        <template v-slot="props">
                            {{ props.row.category }}
                        </template>
                    </b-table-column>
                    <b-table-column
                        field="operation_type"
                        label="Type"
                        sortable
                        searchable
                        centered
                    >
                        <template #searchable="props">
                            <b-field>
                                <b-select
                                    v-model="props.filters[props.column.field]"
                                    placeholder="Operation types..."
                                >
                                    <option :value="null"></option>
                                    <option value="ZAKUP PRZY UŻYCIU KARTY">
                                        Zakup przy użyciu karty
                                    </option>
                                    <option value="PŁATNOŚĆ WEB - KOD MOBILNY">
                                        Płatność onilne - kod mobilny
                                    </option>
                                    <option value="PRZELEW WYCHODZĄCY">
                                        Przelew wychodzący
                                    </option>
                                    <option value="PRZELEW PRZYCHODZĄCY">
                                        Przelew przychodzący
                                    </option>
                                    <option value="PRZELEW NA TELEFON PRZYCHODZ. ZEW.">
                                        Przelew na telefon przychodzący zewnętrzny
                                    </option>
                                    <option value="PRZELEW NA TELEFON WYCHODZĄCY ZEW.">
                                        Przelew na telefon wychodzący zewnętrzny
                                    </option>
                                    <option value="PRZELEW PRZYCH. SYSTEMAT. WPŁYW">
                                        Przelew przychodzący systematyczny
                                    </option>
                                    <option value="WYPŁATA W BANKOMACIE">
                                        Wypłata w bankomacie
                                    </option>
                                    <option value="WPŁATA GOTÓWKI WE WPŁATOMACIE">
                                        Wpłata we wpłatomacie
                                    </option>
                                </b-select>
                            </b-field>
                        </template>
                        <template v-slot="props">
                            {{ props.row.operation_type }}
                        </template>
                    </b-table-column>
                    <b-table-column
                        field="value"
                        label="Amount"
                        sortable
                        searchable
                        centered
                    >
                        <template #searchable="props">
                            <div>
                                <b-field group-multiline>
                                    <div>
                                        <b-input
                                            v-model="
                                                props.filters[
                                                    props.column.field + '_min'
                                                ]
                                            "
                                            placeholder="Min."
                                        />
                                    </div>
                                    <div>
                                        <b-input
                                            v-model="
                                                props.filters[
                                                    props.column.field + '_max'
                                                ]
                                            "
                                            placeholder="Max."
                                        />
                                    </div>
                                </b-field>
                            </div>
                        </template>
                        <template v-slot="props">
                            {{ props.row.value }}
                        </template>
                    </b-table-column>
                    <b-table-column
                        field="balance"
                        label="Balance"
                        sortable
                        v-slot="props"
                        centered
                    >
                        {{ props.row.balance }}
                    </b-table-column>
                </template>
                <template slot="detail" slot-scope="props">
                    <strong>Payment details: </strong>
                    {{ props.row.details }}
                </template>
            </b-table>
        </div>
    </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
export default {
    name: "History",
    data() {
        return {
            loading: false,
            perPage: 25,
            sortField: "id",
            sortOrder: "desc",
            defaultSortOrder: "desc",
            filter: "",
            page: 1,
        };
    },
    methods: {
        loadAsyncData() {
            this.loading = true;
            var fetchData = {
                page: this.page,
                ordering: this.sortField,
                user: this.chosenUser.id,
            };
            for (const [key, value] of Object.entries(this.filter)) {
                if (key == "date") {
                    let current_datetime = value;
                    fetchData[key] =
                        current_datetime.getFullYear() +
                        "-" +
                        this.appendLeadingZeroes(current_datetime.getMonth() + 1) +
                        "-" +
                        this.appendLeadingZeroes(current_datetime.getDate());
                } else {
                    fetchData[key] = value;
                }
            }
            if (this.sortOrder == "desc") {
                fetchData["ordering"] = "-".concat(this.sortField);
            }
            this.getCurrentOperation(fetchData)
                .then(() => {
                    this.loading = false;
                })
                .catch(() => {
                    this.$buefy.notification.open({
                        duration: 5000,
                        message:
                            "Unable to load data from database, check internet connection.",
                        type: "is-danger",
                    });
                });
        },
        onPageChange(num) {
            this.page = num;
            this.loadAsyncData();
        },
        onSort(field, order) {
            this.sortField = field;
            this.sortOrder = order;
            this.loadAsyncData();
        },
        onFiltersChange(filters) {
            this.filter = Object.fromEntries(
                Object.entries(filters).filter(([_, v]) => v !== null && v !== "") // eslint-disable-line no-unused-vars
            );
            this.loadAsyncData();
        },
        appendLeadingZeroes(n) {
            if (n <= 9) {
                return "0" + n;
            }
            return n;
        },
        ...mapActions("operation", ["getCurrentOperation"]),
        ...mapMutations("user", ["setChosenUser"]),
    },
    computed: {
        ...mapState("operation", ["currentOperation", "paginationCount"]),
        ...mapState("user", ["chosenUser"]),
    },
    created() {
        this.loadAsyncData();
    },
};
</script>

<style>
.background {
    background-color: rgb(255, 255, 255);
    width: 400%;
}
</style>
