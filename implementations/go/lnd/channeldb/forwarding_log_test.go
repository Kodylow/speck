package channeldb

import (
	"math/rand"
	"reflect"
	"testing"
	"time"

	"github.com/davecgh/go-spew/spew"
	"github.com/lightningnetwork/lnd/lnwire"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// TestForwardingLogBasicStorageAndQuery tests that we're able to store and
// then query for items that have previously been added to the event log.
func TestForwardingLogBasicStorageAndQuery(t *testing.T) {
	t.Parallel()

	// First, we'll set up a test database, and use that to instantiate the
	// forwarding event log that we'll be using for the duration of the
	// test.
	db, err := MakeTestDB(t)
	require.NoError(t, err, "unable to make test db")

	log := ForwardingLog{
		db: db,
	}

	initialTime := time.Unix(1234, 0)
	timestamp := time.Unix(1234, 0)

	// We'll create 100 random events, which each event being spaced 10
	// minutes after the prior event.
	numEvents := 100
	events := make([]ForwardingEvent, numEvents)
	for i := 0; i < numEvents; i++ {
		events[i] = ForwardingEvent{
			Timestamp:      timestamp,
			IncomingChanID: lnwire.NewShortChanIDFromInt(uint64(rand.Int63())),
			OutgoingChanID: lnwire.NewShortChanIDFromInt(uint64(rand.Int63())),
			AmtIn:          lnwire.MilliSatoshi(rand.Int63()),
			AmtOut:         lnwire.MilliSatoshi(rand.Int63()),
		}

		timestamp = timestamp.Add(time.Minute * 10)
	}

	// Now that all of our set of events constructed, we'll add them to the
	// database in a batch manner.
	if err := log.AddForwardingEvents(events); err != nil {
		t.Fatalf("unable to add events: %v", err)
	}

	// With our events added we'll now construct a basic query to retrieve
	// all of the events.
	eventQuery := ForwardingEventQuery{
		StartTime:    initialTime,
		EndTime:      timestamp,
		IndexOffset:  0,
		NumMaxEvents: 1000,
	}
	timeSlice, err := log.Query(eventQuery)
	require.NoError(t, err, "unable to query for events")

	// The set of returned events should match identically, as they should
	// be returned in sorted order.
	if !reflect.DeepEqual(events, timeSlice.ForwardingEvents) {
		t.Fatalf("event mismatch: expected %v vs %v",
			spew.Sdump(events), spew.Sdump(timeSlice.ForwardingEvents))
	}

	// The offset index of the final entry should be numEvents, so the
	// number of total events we've written.
	if timeSlice.LastIndexOffset != uint32(numEvents) {
		t.Fatalf("wrong final offset: expected %v, got %v",
			timeSlice.LastIndexOffset, numEvents)
	}
}

// TestForwardingLogQueryOptions tests that the query offset works properly. So
// if we add a series of events, then we should be able to seek within the
// timeslice accordingly. This exercises the index offset and num max event
// field in the query, and also the last index offset field int he response.
func TestForwardingLogQueryOptions(t *testing.T) {
	t.Parallel()

	// First, we'll set up a test database, and use that to instantiate the
	// forwarding event log that we'll be using for the duration of the
	// test.
	db, err := MakeTestDB(t)
	require.NoError(t, err, "unable to make test db")

	log := ForwardingLog{
		db: db,
	}

	initialTime := time.Unix(1234, 0)
	endTime := time.Unix(1234, 0)

	// We'll create 20 random events, which each event being spaced 10
	// minutes after the prior event.
	numEvents := 20
	events := make([]ForwardingEvent, numEvents)
	for i := 0; i < numEvents; i++ {
		events[i] = ForwardingEvent{
			Timestamp:      endTime,
			IncomingChanID: lnwire.NewShortChanIDFromInt(uint64(rand.Int63())),
			OutgoingChanID: lnwire.NewShortChanIDFromInt(uint64(rand.Int63())),
			AmtIn:          lnwire.MilliSatoshi(rand.Int63()),
			AmtOut:         lnwire.MilliSatoshi(rand.Int63()),
		}

		endTime = endTime.Add(time.Minute * 10)
	}

	// Now that all of our set of events constructed, we'll add them to the
	// database in a batch manner.
	if err := log.AddForwardingEvents(events); err != nil {
		t.Fatalf("unable to add events: %v", err)
	}

	// With all of our events added, we should be able to query for the
	// first 10 events using the max event query field.
	eventQuery := ForwardingEventQuery{
		StartTime:    initialTime,
		EndTime:      endTime,
		IndexOffset:  0,
		NumMaxEvents: 10,
	}
	timeSlice, err := log.Query(eventQuery)
	require.NoError(t, err, "unable to query for events")

	// We should get exactly 10 events back.
	if len(timeSlice.ForwardingEvents) != 10 {
		t.Fatalf("wrong number of events: expected %v, got %v", 10,
			len(timeSlice.ForwardingEvents))
	}

	// The set of events returned should be the first 10 events that we
	// added.
	if !reflect.DeepEqual(events[:10], timeSlice.ForwardingEvents) {
		t.Fatalf("wrong response: expected %v, got %v",
			spew.Sdump(events[:10]),
			spew.Sdump(timeSlice.ForwardingEvents))
	}

	// The final offset should be the exact number of events returned.
	if timeSlice.LastIndexOffset != 10 {
		t.Fatalf("wrong index offset: expected %v, got %v", 10,
			timeSlice.LastIndexOffset)
	}

	// If we use the final offset to query again, then we should get 10
	// more events, that are the last 10 events we wrote.
	eventQuery.IndexOffset = 10
	timeSlice, err = log.Query(eventQuery)
	require.NoError(t, err, "unable to query for events")

	// We should get exactly 10 events back once again.
	if len(timeSlice.ForwardingEvents) != 10 {
		t.Fatalf("wrong number of events: expected %v, got %v", 10,
			len(timeSlice.ForwardingEvents))
	}

	// The events that we got back should be the last 10 events that we
	// wrote out.
	if !reflect.DeepEqual(events[10:], timeSlice.ForwardingEvents) {
		t.Fatalf("wrong response: expected %v, got %v",
			spew.Sdump(events[10:]),
			spew.Sdump(timeSlice.ForwardingEvents))
	}

	// Finally, the last index offset should be 20, or the number of
	// records we've written out.
	if timeSlice.LastIndexOffset != 20 {
		t.Fatalf("wrong index offset: expected %v, got %v", 20,
			timeSlice.LastIndexOffset)
	}
}

// TestForwardingLogQueryLimit tests that we're able to properly limit the
// number of events that are returned as part of a query.
func TestForwardingLogQueryLimit(t *testing.T) {
	t.Parallel()

	// First, we'll set up a test database, and use that to instantiate the
	// forwarding event log that we'll be using for the duration of the
	// test.
	db, err := MakeTestDB(t)
	require.NoError(t, err, "unable to make test db")

	log := ForwardingLog{
		db: db,
	}

	initialTime := time.Unix(1234, 0)
	endTime := time.Unix(1234, 0)

	// We'll create 200 random events, which each event being spaced 10
	// minutes after the prior event.
	numEvents := 200
	events := make([]ForwardingEvent, numEvents)
	for i := 0; i < numEvents; i++ {
		events[i] = ForwardingEvent{
			Timestamp:      endTime,
			IncomingChanID: lnwire.NewShortChanIDFromInt(uint64(rand.Int63())),
			OutgoingChanID: lnwire.NewShortChanIDFromInt(uint64(rand.Int63())),
			AmtIn:          lnwire.MilliSatoshi(rand.Int63()),
			AmtOut:         lnwire.MilliSatoshi(rand.Int63()),
		}

		endTime = endTime.Add(time.Minute * 10)
	}

	// Now that all of our set of events constructed, we'll add them to the
	// database in a batch manner.
	if err := log.AddForwardingEvents(events); err != nil {
		t.Fatalf("unable to add events: %v", err)
	}

	// Once the events have been written out, we'll issue a query over the
	// entire range, but restrict the number of events to the first 100.
	eventQuery := ForwardingEventQuery{
		StartTime:    initialTime,
		EndTime:      endTime,
		IndexOffset:  0,
		NumMaxEvents: 100,
	}
	timeSlice, err := log.Query(eventQuery)
	require.NoError(t, err, "unable to query for events")

	// We should get exactly 100 events back.
	if len(timeSlice.ForwardingEvents) != 100 {
		t.Fatalf("wrong number of events: expected %v, got %v", 10,
			len(timeSlice.ForwardingEvents))
	}

	// The set of events returned should be the first 100 events that we
	// added.
	if !reflect.DeepEqual(events[:100], timeSlice.ForwardingEvents) {
		t.Fatalf("wrong response: expected %v, got %v",
			spew.Sdump(events[:100]),
			spew.Sdump(timeSlice.ForwardingEvents))
	}

	// The final offset should be the exact number of events returned.
	if timeSlice.LastIndexOffset != 100 {
		t.Fatalf("wrong index offset: expected %v, got %v", 100,
			timeSlice.LastIndexOffset)
	}
}

// TestForwardingLogMakeUniqueTimestamps makes sure the function that creates
// unique timestamps does it job correctly.
func TestForwardingLogMakeUniqueTimestamps(t *testing.T) {
	t.Parallel()

	// Create a list of events where some of the timestamps collide. We
	// expect no existing timestamp to be overwritten, instead the "gaps"
	// between them should be filled.
	inputSlice := []ForwardingEvent{
		{Timestamp: time.Unix(0, 1001)},
		{Timestamp: time.Unix(0, 2001)},
		{Timestamp: time.Unix(0, 1001)},
		{Timestamp: time.Unix(0, 1002)},
		{Timestamp: time.Unix(0, 1004)},
		{Timestamp: time.Unix(0, 1004)},
		{Timestamp: time.Unix(0, 1007)},
		{Timestamp: time.Unix(0, 1001)},
	}
	expectedSlice := []ForwardingEvent{
		{Timestamp: time.Unix(0, 1001)},
		{Timestamp: time.Unix(0, 1002)},
		{Timestamp: time.Unix(0, 1003)},
		{Timestamp: time.Unix(0, 1004)},
		{Timestamp: time.Unix(0, 1005)},
		{Timestamp: time.Unix(0, 1006)},
		{Timestamp: time.Unix(0, 1007)},
		{Timestamp: time.Unix(0, 2001)},
	}

	makeUniqueTimestamps(inputSlice)

	for idx, in := range inputSlice {
		expect := expectedSlice[idx]
		assert.Equal(
			t, expect.Timestamp.UnixNano(), in.Timestamp.UnixNano(),
		)
	}
}

// TestForwardingLogStoreEvent makes sure forwarding events are stored without
// colliding on duplicate timestamps.
func TestForwardingLogStoreEvent(t *testing.T) {
	t.Parallel()

	// First, we'll set up a test database, and use that to instantiate the
	// forwarding event log that we'll be using for the duration of the
	// test.
	db, err := MakeTestDB(t)
	require.NoError(t, err, "unable to make test db")

	log := ForwardingLog{
		db: db,
	}

	// We'll create 20 random events, with each event having a timestamp
	// with just one nanosecond apart.
	numEvents := 20
	events := make([]ForwardingEvent, numEvents)
	ts := time.Now().UnixNano()
	for i := 0; i < numEvents; i++ {
		events[i] = ForwardingEvent{
			Timestamp:      time.Unix(0, ts+int64(i)),
			IncomingChanID: lnwire.NewShortChanIDFromInt(uint64(rand.Int63())),
			OutgoingChanID: lnwire.NewShortChanIDFromInt(uint64(rand.Int63())),
			AmtIn:          lnwire.MilliSatoshi(rand.Int63()),
			AmtOut:         lnwire.MilliSatoshi(rand.Int63()),
		}
	}

	// Now that all of our events are constructed, we'll add them to the
	// database in a batched manner.
	if err := log.AddForwardingEvents(events); err != nil {
		t.Fatalf("unable to add events: %v", err)
	}

	// Because timestamps are de-duplicated when adding them in a single
	// batch before they even hit the DB, we add the same events again but
	// in a new batch. They now have to be de-duplicated on the DB level.
	if err := log.AddForwardingEvents(events); err != nil {
		t.Fatalf("unable to add second batch of events: %v", err)
	}

	// With all of our events added, we should be able to query for all
	// events with a range of just 40 nanoseconds (2 times 20 events, all
	// spaced one nanosecond apart).
	eventQuery := ForwardingEventQuery{
		StartTime:    time.Unix(0, ts),
		EndTime:      time.Unix(0, ts+int64(numEvents*2)),
		IndexOffset:  0,
		NumMaxEvents: uint32(numEvents * 3),
	}
	timeSlice, err := log.Query(eventQuery)
	require.NoError(t, err, "unable to query for events")

	// We should get exactly 40 events back.
	if len(timeSlice.ForwardingEvents) != numEvents*2 {
		t.Fatalf("wrong number of events: expected %v, got %v",
			numEvents*2, len(timeSlice.ForwardingEvents))
	}

	// The timestamps should be spaced out evenly and in order.
	for i := 0; i < numEvents*2; i++ {
		eventTs := timeSlice.ForwardingEvents[i].Timestamp.UnixNano()
		if eventTs != ts+int64(i) {
			t.Fatalf("unexpected timestamp of event %d: expected "+
				"%d, got %d", i, ts+int64(i), eventTs)
		}
	}
}
